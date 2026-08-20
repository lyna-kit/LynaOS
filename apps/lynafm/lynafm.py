#!/usr/bin/env python3

import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path


APP_NAME = "LynaFM"
APP_VERSION = "0.4"

ROOT = Path(__file__).resolve().parents[2]

MUSIC_DIR = ROOT / "music"
DATA_DIR = ROOT / "data"
PLAYLIST_FILE = DATA_DIR / "lynafm_playlist.json"

playlist = []
current_index = -1

player = None
ipc_socket = None
ipc_path = None

current_title = ""
current_source = ""
current_local = False


# ============================================================
# UTILIDADES
# ============================================================

def command_exists(command):
    return shutil.which(command) is not None


def clear():
    os.system("clear")


# ============================================================
# DEPENDENCIAS
# ============================================================

def check_dependencies():

    missing = []

    if not command_exists("mpv"):
        missing.append("mpv")

    if not command_exists("yt-dlp"):
        missing.append("yt-dlp")

    if missing:

        print(
            "Dependencias faltantes: "
            + ", ".join(missing)
        )

        print()

        if "mpv" in missing:
            print("Instala MPV con:")
            print("pkg install mpv")

        if "yt-dlp" in missing:
            print("Instala yt-dlp con:")
            print(
                "python -m pip install -U yt-dlp"
            )

        return False

    return True


# ============================================================
# PERSISTENCIA
# ============================================================

def load_playlist():

    global playlist

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not PLAYLIST_FILE.exists():

        playlist = []

        return

    try:

        with open(
            PLAYLIST_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):

            playlist = data

        else:

            playlist = []

    except Exception:

        playlist = []


def save_playlist():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        with open(
            PLAYLIST_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                playlist,
                file,
                ensure_ascii=False,
                indent=2
            )

    except Exception as error:

        print(
            f"✗ Error guardando lista: {error}"
        )


# ============================================================
# BANNER
# ============================================================

def banner():

    print(
        f"""
╔══════════════════════════════════════╗
║             {APP_NAME} {APP_VERSION}             ║
║          Música de LynaOS            ║
╚══════════════════════════════════════╝
"""
    )

    if current_title:

        print(
            f"▶ Reproduciendo: {current_title}"
        )

        print()


# ============================================================
# AYUDA
# ============================================================

def help_command():

    print("""
LynaFM 0.4

LIST       Lista de enlaces
LOCAL      Música descargada
ADD        Añadir enlace
DOWNLOAD   Descargar

L 1        Reproducir enlace #1
M 1        Reproducir archivo local #1

N          Siguiente
B          Anterior
P          Pausa / reanudar
S          Detener
R          Reiniciar

←          -5 segundos
→          +5 segundos

REMOVE 1   Quitar canción
CLEAR      Limpiar lista

HELP       Ayuda
Q          Salir
""")


# ============================================================
# IPC MPV
# ============================================================

def connect_ipc(path):

    global ipc_socket

    try:

        sock = socket.socket(
            socket.AF_UNIX,
            socket.SOCK_STREAM
        )

        sock.connect(path)

        ipc_socket = sock

        return True

    except Exception:

        ipc_socket = None

        return False


def send_mpv(command):

    global ipc_socket

    if ipc_socket is None:

        return False

    try:

        message = json.dumps({
            "command": command
        }) + "\n"

        ipc_socket.sendall(
            message.encode("utf-8")
        )

        return True

    except Exception:

        try:
            ipc_socket.close()
        except Exception:
            pass

        ipc_socket = None

        return False


# ============================================================
# ESTADO MPV
# ============================================================

def player_running():

    return (
        player is not None
        and player.poll() is None
    )


# ============================================================
# INICIAR MPV
# ============================================================

def start_mpv(
    source,
    title,
    local=False
):

    global player
    global ipc_socket
    global ipc_path

    global current_title
    global current_source
    global current_local

    stop_player()

    socket_path = (
        Path(tempfile.gettempdir())
        / f"lynafm-{os.getpid()}.sock"
    )

    try:

        if socket_path.exists():

            socket_path.unlink()

    except Exception:
        pass

    ipc_path = str(socket_path)

    try:

        player = subprocess.Popen(
            [
                "mpv",
                "--no-video",
                "--force-window=no",
                "--idle=no",
                f"--input-ipc-server={ipc_path}",
                source
            ]
        )

    except Exception as error:

        print(
            f"✗ Error iniciando MPV: {error}"
        )

        player = None

        return False

    for _ in range(40):

        if socket_path.exists():

            break

        if player.poll() is not None:

            break

        time.sleep(0.1)

    if not socket_path.exists():

        print(
            "✗ MPV no creó el socket."
        )

        stop_player()

        return False

    if not connect_ipc(
        str(socket_path)
    ):

        print(
            "✗ No se pudo conectar con MPV."
        )

        stop_player()

        return False

    current_title = title
    current_source = source
    current_local = local

    return True


# ============================================================
# DETENER MPV
# ============================================================

def stop_player():

    global player
    global ipc_socket
    global ipc_path

    global current_title
    global current_source
    global current_local

    if ipc_socket:

        try:

            ipc_socket.close()

        except Exception:
            pass

    ipc_socket = None

    if player:

        try:

            if player.poll() is None:

                player.terminate()

                player.wait(
                    timeout=2
                )

        except Exception:

            try:
                player.kill()

            except Exception:
                pass

    player = None

    if ipc_path:

        try:

            path = Path(ipc_path)

            if path.exists():

                path.unlink()

        except Exception:
            pass

    ipc_path = None

    current_title = ""
    current_source = ""
    current_local = False


# ============================================================
# OBTENER AUDIO DE YOUTUBE
# ============================================================

def get_audio_url(url):

    print(
        "Obteniendo flujo de audio..."
    )

    try:

        result = subprocess.run(
            [
                "yt-dlp",
                "--no-playlist",
                "-f",
                "bestaudio/best",
                "-g",
                url
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

    except subprocess.TimeoutExpired:

        print(
            "✗ Tiempo de espera agotado."
        )

        return None

    except Exception as error:

        print(
            f"✗ Error ejecutando yt-dlp: {error}"
        )

        return None

    if result.returncode != 0:

        print(
            "✗ yt-dlp no pudo obtener "
            "el audio."
        )

        if result.stderr:

            print(
                result.stderr.strip()
            )

        return None

    audio_url = result.stdout.strip()

    if not audio_url:

        print(
            "✗ No se obtuvo ningún flujo."
        )

        return None

    return audio_url


# ============================================================
# LISTA DE ENLACES
# ============================================================

def show_list():

    if not playlist:

        print(
            "No hay enlaces guardados."
        )

        return

    print("""
╔══════════════════════════════════════╗
║             LISTA LynaFM             ║
╚══════════════════════════════════════╝
""")

    for index, item in enumerate(
        playlist,
        start=1
    ):

        title = item.get(
            "title",
            "Sin título"
        )

        marker = (
            "▶ "
            if index - 1 == current_index
            else "  "
        )

        print(
            f"{marker}{index}. {title}"
        )


# ============================================================
# MÚSICA LOCAL
# ============================================================

def get_local_files():

    if not MUSIC_DIR.exists():

        return []

    extensions = {
        ".mp3",
        ".m4a",
        ".opus",
        ".ogg",
        ".wav",
        ".flac",
        ".aac",
        ".webm"
    }

    files = []

    for file in MUSIC_DIR.iterdir():

        if (
            file.is_file()
            and file.suffix.lower()
            in extensions
        ):

            files.append(file)

    return sorted(
        files,
        key=lambda file:
        file.name.lower()
    )


def show_local():

    files = get_local_files()

    if not files:

        print(
            "No hay música descargada."
        )

        print(
            f"Directorio: {MUSIC_DIR}"
        )

        return

    print("""
╔══════════════════════════════════════╗
║          MÚSICA DESCARGADA           ║
╚══════════════════════════════════════╝
""")

    for index, file in enumerate(
        files,
        start=1
    ):

        print(
            f"{index}. {file.name}"
        )


# ============================================================
# AÑADIR ENLACE
# ============================================================

def add_song():

    title = input(
        "Nombre de la canción> "
    ).strip()

    if not title:

        print(
            "Nombre inválido."
        )

        return

    url = input(
        "URL de YouTube> "
    ).strip()

    if (
        "youtube.com/" not in url
        and "youtu.be/" not in url
    ):

        print(
            "Solo se aceptan enlaces "
            "de YouTube."
        )

        return

    playlist.append({
        "title": title,
        "url": url
    })

    save_playlist()

    print(
        f"✓ Añadida: {title}"
    )


# ============================================================
# REPRODUCIR ENLACE
# ============================================================

def play_song(index):

    global current_index

    if not playlist:

        print(
            "La lista está vacía."
        )

        return

    if index < 0 or index >= len(playlist):

        print(
            "Canción inexistente."
        )

        return

    if not check_dependencies():

        return

    item = playlist[index]

    title = item.get(
        "title",
        "Sin título"
    )

    url = item.get(
        "url",
        ""
    )

    audio_url = get_audio_url(
        url
    )

    if not audio_url:

        return

    if start_mpv(
        audio_url,
        title,
        False
    ):

        current_index = index

        print()
        print(
            f"▶ Reproduciendo: {title}"
        )


# ============================================================
# REPRODUCIR LOCAL
# ============================================================

def play_local(index):

    files = get_local_files()

    if not files:

        print(
            "No hay música descargada."
        )

        return

    if index < 0 or index >= len(files):

        print(
            "Archivo inexistente."
        )

        return

    file = files[index]

    if not command_exists("mpv"):

        print(
            "MPV no está instalado."
        )

        return

    if start_mpv(
        str(file),
        file.name,
        True
    ):

        print()
        print(
            f"▶ Reproduciendo: {file.name}"
        )


# ============================================================
# PLAY / PAUSE
# ============================================================

def toggle_pause():

    if not player_running():

        print(
            "No hay reproducción."
        )

        return

    if send_mpv([
        "cycle",
        "pause"
    ]):

        print(
            "✓ Pausa / reproducción cambiada."
        )

    else:

        print(
            "✗ No se pudo controlar MPV."
        )


# ============================================================
# DETENER
# ============================================================

def stop():

    if not player_running():

        print(
            "No hay reproducción."
        )

        return

    stop_player()

    print(
        "■ Reproducción detenida."
    )


# ============================================================
# REINICIAR
# ============================================================

def restart_song():

    if not player_running():

        print(
            "No hay reproducción."
        )

        return

    if send_mpv([
        "set",
        "time-pos",
        0
    ]):

        print(
            "↻ Canción reiniciada."
        )

    else:

        print(
            "✗ No se pudo reiniciar."
        )


# ============================================================
# ADELANTAR 5 SEGUNDOS
# ============================================================

def forward():

    if not player_running():

        print(
            "No hay reproducción."
        )

        return

    if send_mpv([
        "seek",
        5,
        "relative"
    ]):

        print(
            "→ +5 segundos."
        )

    else:

        print(
            "✗ No se pudo adelantar."
        )


# ============================================================
# RETROCEDER 5 SEGUNDOS
# ============================================================

def backward():

    if not player_running():

        print(
            "No hay reproducción."
        )

        return

    if send_mpv([
        "seek",
        -5,
        "relative"
    ]):

        print(
            "← -5 segundos."
        )

    else:

        print(
            "✗ No se pudo retroceder."
        )


# ============================================================
# SIGUIENTE
# ============================================================

def next_song():

    if not playlist:

        print(
            "La lista está vacía."
        )

        return

    next_index = current_index + 1

    if next_index >= len(playlist):

        print(
            "No hay siguiente canción."
        )

        return

    play_song(
        next_index
    )


# ============================================================
# ANTERIOR
# ============================================================

def previous_song():

    if not playlist:

        print(
            "La lista está vacía."
        )

        return

    previous_index = current_index - 1

    if previous_index < 0:

        print(
            "No hay canción anterior."
        )

        return

    play_song(
        previous_index
    )


# ============================================================
# DESCARGAR
# ============================================================

def download_song(index):

    if not playlist:

        print(
            "La lista está vacía."
        )

        return

    if index < 0 or index >= len(playlist):

        print(
            "Canción inexistente."
        )

        return

    if not command_exists("yt-dlp"):

        print(
            "yt-dlp no está instalado."
        )

        return

    MUSIC_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    item = playlist[index]

    title = item.get(
        "title",
        "Sin título"
    )

    url = item.get(
        "url",
        ""
    )

    print()
    print(
        f"⬇ Descargando: {title}"
    )

    output = str(
        MUSIC_DIR /
        "%(title)s.%(ext)s"
    )

    result = subprocess.run(
        [
            "yt-dlp",
            "--no-playlist",
            "-x",
            "--audio-format",
            "mp3",
            "-o",
            output,
            url
        ],
        check=False
    )

    if result.returncode == 0:

        print()
        print(
            "✓ Descarga completada."
        )

    else:

        print()
        print(
            "✗ La descarga no se pudo completar."
        )


# ============================================================
# REMOVE
# ============================================================

def remove_song(index):

    if index < 0 or index >= len(playlist):

        print(
            "Canción inexistente."
        )

        return

    item = playlist.pop(
        index
    )

    save_playlist()

    print(
        "✓ Eliminada: "
        + item.get(
            "title",
            "Sin título"
        )
    )


# ============================================================
# CLEAR
# ============================================================

def clear_playlist():

    playlist.clear()

    save_playlist()

    print(
        "✓ Lista limpiada."
    )


# ============================================================
# PROCESAR COMANDOS
# ============================================================

def process_command(command):

    global current_index

    parts = command.strip().split()

    if not parts:

        return True

    action = parts[0].upper()

    # --------------------------------------------------------
    # SALIR
    # --------------------------------------------------------

    if action in (
        "Q",
        "EXIT"
    ):

        stop_player()

        print(
            "Saliendo de LynaFM..."
        )

        return False

    # --------------------------------------------------------
    # AYUDA
    # --------------------------------------------------------

    if action in (
        "HELP",
        "H"
    ):

        help_command()

        return True

    # --------------------------------------------------------
    # LISTA
    # --------------------------------------------------------

    if action == "LIST":

        show_list()

        return True

    # --------------------------------------------------------
    # LOCAL
    # --------------------------------------------------------

    if action == "LOCAL":

        show_local()

        return True

    # --------------------------------------------------------
    # ADD
    # --------------------------------------------------------

    if action == "ADD":

        add_song()

        return True

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    if action == "DOWNLOAD":

        if len(parts) != 2:

            print(
                "Uso: DOWNLOAD <número>"
            )

            return True

        try:

            index = int(parts[1]) - 1

        except ValueError:

            print(
                "Número inválido."
            )

            return True

        download_song(index)

        return True

    # --------------------------------------------------------
    # LISTEN
    # --------------------------------------------------------

    if action == "L":

        if len(parts) != 2:

            print(
                "Uso: L <número>"
            )

            return True

        try:

            index = int(parts[1]) - 1

        except ValueError:

            print(
                "Número inválido."
            )

            return True

        play_song(index)

        return True

    # --------------------------------------------------------
    # LOCAL PLAY
    # --------------------------------------------------------

    if action == "M":

        if len(parts) != 2:

            print(
                "Uso: M <número>"
            )

            return True

        try:

            index = int(parts[1]) - 1

        except ValueError:

            print(
                "Número inválido."
            )

            return True

        play_local(index)

        return True

    # --------------------------------------------------------
    # SIGUIENTE
    # --------------------------------------------------------

    if action == "N":

        next_song()

        return True

    # --------------------------------------------------------
    # ANTERIOR
    # --------------------------------------------------------

    if action == "B":

        previous_song()

        return True

    # --------------------------------------------------------
    # PAUSA
    # --------------------------------------------------------

    if action == "P":

        toggle_pause()

        return True

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    if action == "S":

        stop()

        return True

    # --------------------------------------------------------
    # RESTART
    # --------------------------------------------------------

    if action == "R":

        restart_song()

        return True

    # --------------------------------------------------------
    # FLECHA DERECHA
    # --------------------------------------------------------

    if command == "→":

        forward()

        return True

    # --------------------------------------------------------
    # FLECHA IZQUIERDA
    # --------------------------------------------------------

    if command == "←":

        backward()

        return True

    # --------------------------------------------------------
    # REMOVE
    # --------------------------------------------------------

    if action == "REMOVE":

        if len(parts) != 2:

            print(
                "Uso: REMOVE <número>"
            )

            return True

        try:

            index = int(parts[1]) - 1

        except ValueError:

            print(
                "Número inválido."
            )

            return True

        remove_song(index)

        return True

    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    if action == "CLEAR":

        clear_playlist()

        return True

    # --------------------------------------------------------
    # CLEAR SCREEN
    # --------------------------------------------------------

    if action == "CLS":

        clear()

        return True

    # --------------------------------------------------------
    # DESCONOCIDO
    # --------------------------------------------------------

    print(
        "Comando desconocido."
    )

    print(
        "Escribe HELP para ver los comandos."
    )

    return True


# ============================================================
# MAIN
# ============================================================

def run():

    global current_index

    load_playlist()

    clear()

    banner()

    print(
        "Escribe HELP para ver los comandos."
    )

    print()

    while True:

        try:

            command = input(
                "lynafm> "
            )

            if not process_command(
                command
            ):

                break

            print()

        except KeyboardInterrupt:

            print()

            print(
                "Usa Q para salir de LynaFM."
            )

            print()

        except EOFError:

            stop_player()

            print()

            break


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    run()
