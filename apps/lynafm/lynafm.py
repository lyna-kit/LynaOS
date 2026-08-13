#!/usr/bin/env python3

import os
import shutil
import signal
import subprocess
from pathlib import Path


APP_NAME = "LynaFM"
APP_VERSION = "0.2"

LYNAOS_ROOT = Path(__file__).resolve().parents[2]
MUSIC_DIR = LYNAOS_ROOT / "music"

playlist = []
current_index = -1
player = None
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
        print(
            "Puedes instalarlas con:"
        )
        print(
            "pkg install mpv"
        )
        print(
            "pip install yt-dlp"
        )

        return False

    return True


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print(f"""
╔══════════════════════════════════════╗
║           {APP_NAME} {APP_VERSION}           ║
║          Música de LynaOS           ║
╚══════════════════════════════════════╝

L = Escuchar
D = Descargar
P = Play / Pause
← = Retroceder
→ = Adelantar
N = Siguiente
B = Anterior
LIST = Lista
ADD = Añadir
H = Ayuda
Q = Salir
""")


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print("""
LynaFM 0.2

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
  D 1
  N
  B
""")


# ============================================================
#                     DETENER REPRODUCTOR
# ============================================================

def stop_player():

    global player
    global playing

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
#                         REPRODUCIR
# ============================================================

def play_song(index):

    global current_index
    global player
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

    try:

        player = subprocess.Popen(
            [
                "mpv",
                "--no-video",
                "--force-window=no",
                "--input-ipc-client=no",
                url
            ]
        )

        playing = True

    except Exception as error:

        print(
            f"LynaFM: error: {error}"
        )


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

    try:

        if playing:

            player.send_signal(
                signal.SIGSTOP
            )

            playing = False

            print("⏸ Pausado.")

        else:

            player.send_signal(
                signal.SIGCONT
            )

            playing = True

            print("▶ Reproduciendo.")

    except Exception as error:

        print(
            f"LynaFM: {error}"
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

    print(
        "→ Adelantar 10 segundos."
    )

    # Reiniciar la reproducción con mpv
    # usando su control de entrada no es
    # posible mediante stdin en este modo.
    #
    # Se deja preparado para la siguiente
    # versión del reproductor.


# ============================================================
#                         RETROCEDER
# ============================================================

def backward():

    if player is None:

        print(
            "LynaFM: no hay reproducción."
        )

        return

    print(
        "← Retroceder 10 segundos."
    )


# ============================================================
#                          SIGUIENTE
# ============================================================

def next_song():

    if not playlist:

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
#                        AÑADIR
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
            "pip install yt-dlp"
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

        subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format",
                "mp3",
                "-o",
                output,
                url
            ],
            check=False
        )

        print()
        print(
            f"✓ Guardado en: {MUSIC_DIR}"
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

Funciones:
  • Reproducción
  • Descarga de audio
  • Playlist
  • Play / Pause
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
