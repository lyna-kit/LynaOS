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
APP_VERSION = "0.3"

LYNAOS_ROOT = Path(__file__).resolve().parents[2]
MUSIC_DIR = LYNAOS_ROOT / "music"

playlist = []
current_index = -1

player = None
ipc_socket = None
playing = False


# ============================================================
#                         UTILIDADES
# ============================================================

def command_exists(command):
    return shutil.which(command) is not None


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
        print("Instala las dependencias con:")

        if "mpv" in missing:
            print("pkg install mpv")

        if "yt-dlp" in missing:
            print("python -m pip install -U yt-dlp")

        return False

    return True


def create_ipc_path():

    return str(
        Path(tempfile.gettempdir())
        / "lynafm-mpv.sock"
    )


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print(f"""
╔══════════════════════════════════════╗
║           {APP_NAME} {APP_VERSION}           ║
║          Música de LynaOS           ║
╚══════════════════════════════════════╝

L <número> = Escuchar
D <número> = Descargar
P          = Play / Pause
←          = Retroceder 10 segundos
→          = Adelantar 10 segundos
N          = Siguiente
B          = Anterior
LIST       = Lista
ADD        = Añadir enlace de YouTube
H          = Ayuda
ABOUT      = Información
CLEAR      = Limpiar pantalla
Q          = Salir
""")


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print("""
LynaFM 0.3

Comandos:

  L <número>       Escuchar canción
  D <número>       Descargar canción
  P                Play / Pause
  ←                Retroceder 10 segundos
  →                Adelantar 10 segundos
  N                Siguiente
  B                Anterior
  LIST             Mostrar lista
  ADD              Añadir enlace de YouTube
  H                Ayuda
  ABOUT            Información
  CLEAR            Limpiar pantalla
  Q                Salir

Ejemplos:

  ADD
  LIST
  L 1
  P
  →
  ←
  N
  B
  D 1
""")


# ============================================================
#                       IPC DE MPV
# ============================================================

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

        return False


def connect_ipc():

    global ipc_socket

    if ipc_socket is None:
        return False

    for _ in range(20):

        try:

            sock = socket.socket(
                socket.AF_UNIX,
                socket.SOCK_STREAM
            )

            sock.connect(ipc_socket)

            ipc_socket = sock

            return True

        except Exception:

            time.sleep(0.1)

    return False


# ============================================================
#                    DETENER REPRODUCTOR
# ============================================================

def stop_player():

    global player
    global ipc_socket
    global playing

    if ipc_socket is not None:

        try:
            ipc_socket.close()
        except Exception:
            pass

    ipc_socket = None

    if player is not None:

        try:

            player.terminate()
            player.wait(timeout=2)

        except Exception:

            try:
                player.kill()

            except Exception:
                pass

    player = None
    playing = False


# ============================================================
#                     OBTENER AUDIO
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

        error = result.stderr.strip()

        print(
            "✗ yt-dlp no pudo obtener "
            "el audio."
        )

        if "403" in error:

            print()
            print(
                "HTTP 403: el servidor rechazó "
                "la solicitud."
            )

            print(
                "Actualiza yt-dlp:"
            )

            print(
                "python -m pip install -U yt-dlp"
            )

        else:

            if error:
                print(error)

        return None

    audio_url = result.stdout.strip()

    if not audio_url:

        print(
            "✗ No se obtuvo ningún flujo."
        )

        return None

    return audio_url


# ============================================================
#                         REPRODUCIR
# ============================================================

def play_song(index):

    global current_index
    global player
    global ipc_socket
    global playing

    if not playlist:

        print(
            "LynaFM: la lista está vacía."
        )

        return

    if index < 0 or index >= len(playlist):

        print(
            "LynaFM: canción inexistente."
        )

        return

    if not check_dependencies():

        return

    stop_player()

    current_index = index

    title, url = playlist[index]

    print()
    print(
        f"▶ Escuchando: {title}"
    )
    print()

    audio_url = get_audio_url(url)

    if not audio_url:

        return

    socket_path = create_ipc_path()

    try:

        if os.path.exists(socket_path):

            os.remove(socket_path)

    except Exception:
        pass

    ipc_socket = socket_path

    try:

        player = subprocess.Popen(
            [
                "mpv",
                "--no-video",
                "--force-window=no",
                "--idle=no",
                f"--input-ipc-server={socket_path}",
                audio_url
            ]
        )

    except Exception as error:

        print(
            f"LynaFM: error iniciando mpv: {error}"
        )

        ipc_socket = None
        player = None

        return

    # Esperar a que mpv cree el socket.

    socket_path_value = socket_path

    ipc_socket = None

    for _ in range(30):

        if os.path.exists(
            socket_path_value
        ):

            break

        time.sleep(0.1)

    if not os.path.exists(
        socket_path_value
    ):

        print(
            "✗ No se pudo iniciar el "
            "control de mpv."
        )

        stop_player()

        return

    try:

        sock = socket.socket(
            socket.AF_UNIX,
            socket.SOCK_STREAM
        )

        sock.connect(
            socket_path_value
        )

        ipc_socket = sock

    except Exception as error:

        print(
            f"✗ Error conectando con mpv: {error}"
        )

        stop_player()

        return

    playing = True


# ============================================================
#                       PLAY / PAUSE
# ============================================================

def toggle_play():

    global playing

    if player is None:

        if current_index >= 0:

            play_song(current_index)

        elif playlist:

            play_song(0)

        else:

            print(
                "LynaFM: no hay canciones."
            )

        return

    if send_mpv([
        "cycle",
        "pause"
    ]):

        playing = not playing

        if playing:
            print("▶ Reproduciendo.")
        else:
            print("⏸ Pausado.")

    else:

        print(
            "✗ No se pudo controlar mpv."
        )


# ============================================================
#                         ADELANTAR
# ============================================================

def forward():

    if player is None:

        print(
            "LynaFM: no hay reproducción."
        )

        return

    if send_mpv([
        "seek",
        10,
        "relative"
    ]):

        print(
            "→ +10 segundos."
        )

    else:

        print(
            "✗ No se pudo adelantar."
        )


# ============================================================
#                         RETROCEDER
# ============================================================

def backward():

    if player is None:

        print(
            "LynaFM: no hay reproducción."
        )

        return

    if send_mpv([
        "seek",
        -10,
        "relative"
    ]):

        print(
            "← -10 segundos."
        )

    else:

        print(
            "✗ No se pudo retroceder."
        )


# ============================================================
#                          SIGUIENTE
# ============================================================

def next_song():

    if not playlist:

        print(
            "LynaFM: la lista está vacía."
        )

        return

    next_index = current_index + 1

    if next_index >= len(playlist):

        print(
            "LynaFM: no hay siguiente canción."
        )

        return

    play_song(next_index)


# ============================================================
#                          ANTERIOR
# ============================================================

def previous_song():

    if not playlist:

        print(
            "LynaFM: la lista está vacía."
        )

        return

    previous_index = current_index - 1

    if previous_index < 0:

        print(
            "LynaFM: no hay canción anterior."
        )

        return

    play_song(previous_index)


# ============================================================
#                           LISTA
# ============================================================

def show_list():

    if not playlist:

        print(
            "LynaFM: la lista está vacía."
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

        title = item[0]

        marker = "▶" if (
            index - 1 == current_index
        ) else " "

        print(
            f"{marker} {index}. {title}"
        )


# ============================================================
#                           AÑADIR
# ============================================================

def add_song():

    title = input(
        "Nombre de la canción> "
    ).strip()

    if not title:

        print(
            "LynaFM: nombre inválido."
        )

        return

    url = input(
        "URL de YouTube> "
    ).strip()

    if not (
        "youtube.com/" in url
        or "youtu.be/" in url
    ):

        print(
            "LynaFM: solamente se aceptan "
            "enlaces de YouTube."
        )

        return

    playlist.append(
        (
            title,
            url
        )
    )

    print(
        f"✓ Añadida: {title}"
    )


# ============================================================
#                         DESCARGAR
# ============================================================

def download_song(index):

    if not playlist:

        print(
            "LynaFM: la lista está vacía."
        )

        return

    if index < 0 or index >= len(playlist):

        print(
            "LynaFM: canción inexistente."
        )

        return

    if not command_exists("yt-dlp"):

        print(
            "LynaFM: yt-dlp no está instalado."
        )

        print(
            "python -m pip install -U yt-dlp"
        )

        return

    MUSIC_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    title, url = playlist[index]

    print()
    print(
        f"⬇ Descargando: {title}"
    )

    output = str(
        MUSIC_DIR / "%(title)s.%(ext)s"
    )

    try:

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
                f"✓ Guardado en: {MUSIC_DIR}"
            )

        else:

            print()
            print(
                "✗ La descarga no se pudo completar."
            )

    except Exception as error:

        print(
            f"LynaFM: error de descarga: {error}"
        )


# ============================================================
#                           ABOUT
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Reproductor musical de LynaOS.

Fuente:
  YouTube

Motor:
  mpv + yt-dlp

Funciones:
  • Reproducción
  • Descarga de audio
  • Playlist
  • Play / Pause
  • Adelantar
  • Retroceder
  • Siguiente / Anterior

Música descargada:
  {MUSIC_DIR}
""")


# ============================================================
#                           APP
# ============================================================

def run():

    banner()

    while True:

        try:

            command = input(
                "lynafm> "
            ).strip()

            if not command:
                continue

            upper = command.upper()

            # ------------------------------------------------
            # SALIR
            # ------------------------------------------------

            if upper in ("Q", "EXIT"):

                stop_player()

                print(
                    "Saliendo de LynaFM..."
                )

                break

            # ------------------------------------------------
            # AYUDA
            # ------------------------------------------------

            elif upper in ("H", "HELP"):

                help_command()

            # ------------------------------------------------
            # ABOUT
            # ------------------------------------------------

            elif upper == "ABOUT":

                about()

            # ------------------------------------------------
            # CLEAR
            # ------------------------------------------------

            elif upper == "CLEAR":

                os.system("clear")

            # ------------------------------------------------
            # PLAY / PAUSE
            # ------------------------------------------------

            elif upper == "P":

                toggle_play()

            # ------------------------------------------------
            # SIGUIENTE
            # ------------------------------------------------

            elif upper == "N":

                next_song()

            # ------------------------------------------------
            # ANTERIOR
            # ------------------------------------------------

            elif upper == "B":

                previous_song()

            # ------------------------------------------------
            # ADELANTAR
            # ------------------------------------------------

            elif command == "→":

                forward()

            # ------------------------------------------------
            # RETROCEDER
            # ------------------------------------------------

            elif command == "←":

                backward()

            # ------------------------------------------------
            # LIST
            # ------------------------------------------------

            elif upper == "LIST":

                show_list()

            # ------------------------------------------------
            # ADD
            # ------------------------------------------------

            elif upper == "ADD":

                add_song()

            # ------------------------------------------------
            # LISTEN
            # ------------------------------------------------

            elif upper.startswith("L"):

                parts = command.split()

                if len(parts) < 2:

                    print(
                        "Uso: L <número>"
                    )

                    continue

                try:

                    index = int(
                        parts[1]
                    ) - 1

                    play_song(index)

                except ValueError:

                    print(
                        "Número inválido."
                    )

            # ------------------------------------------------
            # DOWNLOAD
            # ------------------------------------------------

            elif upper.startswith("D"):

                parts = command.split()

                if len(parts) < 2:

                    print(
                        "Uso: D <número>"
                    )

                    continue

                try:

                    index = int(
                        parts[1]
                    ) - 1

                    download_song(index)

                except ValueError:

                    print(
                        "Número inválido."
                    )

            else:

                print(
                    "Comando desconocido."
                )

                print(
                    "Escribe H para ver la ayuda."
                )

        except KeyboardInterrupt:

            stop_player()

            print()

        except EOFError:

            stop_player()

            break


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":
    run()
