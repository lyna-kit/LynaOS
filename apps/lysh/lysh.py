#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys


APP_NAME = "Lysh"
APP_VERSION = "0.4"

BASH = shutil.which("bash")


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════════════════════════╗
║                       Lysh 0.4                          ║
║                LynaOS Shell Interface                   ║
╚══════════════════════════════════════════════════════════╝

Lysh utiliza Bash como backend.

Escribe 'help' para ver los comandos especiales.
Escribe 'exit' para volver a LynaOS.
""")


# ============================================================
#                    COMPROBAR ENTORNO
# ============================================================

def check_environment():

    if BASH is None:

        print("✗ Bash no está disponible.")
        print()
        print("En Termux puedes instalarlo con:")
        print()
        print("    pkg install bash")
        print()

        return False

    return True


# ============================================================
#                         AYUDA
# ============================================================

def help_command():

    print("""
============================================================
                         Lysh 0.4
============================================================

Lysh es la interfaz de terminal de LynaOS.

Los comandos normales se ejecutan mediante Bash.

COMANDOS ESPECIALES

  help          Mostrar esta ayuda
  version       Mostrar versión
  clear         Limpiar pantalla
  pwd           Mostrar directorio actual
  cd <ruta>     Cambiar de directorio
  history       Mostrar historial
  whoami        Mostrar usuario actual
  exit          Salir de Lysh
  quit          Salir de Lysh

EJEMPLOS

  ls
  pwd
  cd ..
  mkdir prueba
  touch archivo.txt
  cp archivo.txt copia.txt
  mv copia.txt nueva.txt
  rm archivo.txt
  chmod +x programa.sh
  ./programa.sh
  python programa.py
  git status

Lysh ejecuta los comandos directamente con Bash.
============================================================
""")


# ============================================================
#                         VERSION
# ============================================================

def version():

    print()
    print(f"{APP_NAME} {APP_VERSION}")
    print("LynaOS Shell Interface")
    print()
    print("Backend:")

    if BASH:
        print(f"  Bash: {BASH}")

        try:

            result = subprocess.run(
                [BASH, "--version"],
                capture_output=True,
                text=True
            )

            first_line = result.stdout.splitlines()

            if first_line:
                print(f"  {first_line[0]}")

        except Exception:
            pass

    else:
        print("  Bash: No disponible")

    print()


# ============================================================
#                        HISTORIAL
# ============================================================

command_history = []


def show_history():

    print()

    if not command_history:

        print("El historial está vacío.")
        print()

        return

    for number, command in enumerate(
        command_history,
        start=1
    ):

        print(
            f"{number:>4}  {command}"
        )

    print()


# ============================================================
#                    DIRECTORIO ACTUAL
# ============================================================

def current_directory():

    path = os.getcwd()
    home = os.path.expanduser("~")

    if path == home:

        return "~"

    if path.startswith(home + os.sep):

        return (
            "~" +
            path[len(home):]
        )

    return path


# ============================================================
#                         PROMPT
# ============================================================

def prompt():

    directory = current_directory()

    return (
        "\033[32m"
        "lysh"
        "\033[0m:"
        "\033[34m"
        f"{directory}"
        "\033[0m$ "
    )


# ============================================================
#                    EJECUTAR COMANDO
# ============================================================

def execute(command):

    if BASH is None:

        print(
            "Lysh: Bash no está disponible."
        )

        return 1

    try:

        result = subprocess.run(
            [
                BASH,
                "-c",
                command
            ],
            cwd=os.getcwd()
        )

        return result.returncode

    except KeyboardInterrupt:

        print()

        return 130

    except FileNotFoundError:

        print(
            "Lysh: no se pudo ejecutar Bash."
        )

        return 1

    except Exception as error:

        print(
            f"Lysh: error: {error}"
        )

        return 1


# ============================================================
#                      EJECUTAR CD
# ============================================================

def change_directory(command):

    parts = command.split(maxsplit=1)

    if len(parts) == 1:

        destination = os.path.expanduser("~")

    else:

        destination = parts[1].strip()

        destination = os.path.expanduser(
            destination
        )

    try:

        os.chdir(destination)

    except FileNotFoundError:

        print(
            f"Lysh: directorio no encontrado: {destination}"
        )

    except NotADirectoryError:

        print(
            f"Lysh: no es un directorio: {destination}"
        )

    except PermissionError:

        print(
            f"Lysh: permiso denegado: {destination}"
        )

    except Exception as error:

        print(
            f"Lysh: error: {error}"
        )


# ============================================================
#                     EJECUTAR PWD
# ============================================================

def show_pwd():

    print(
        os.getcwd()
    )


# ============================================================
#                     EJECUTAR WHOAMI
# ============================================================

def show_user():

    try:

        result = subprocess.run(
            [
                BASH,
                "-c",
                "whoami"
            ],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        if output:
            print(output)
        else:
            print(
                os.environ.get(
                    "USER",
                    "unknown"
                )
            )

    except Exception:

        print(
            os.environ.get(
                "USER",
                "unknown"
            )
        )


# ============================================================
#                       LIMPIAR
# ============================================================

def clear_screen():

    os.system("clear")


# ============================================================
#                   PROCESAR COMANDO
# ============================================================

def process_command(command):

    lower = command.lower()

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if lower in (
        "exit",
        "quit"
    ):

        print(
            "Saliendo de Lysh..."
        )

        return False


    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if lower in (
        "help",
        "?"
    ):

        help_command()

        return True


    # --------------------------------------------------------
    # VERSION
    # --------------------------------------------------------

    if lower in (
        "version",
        "--version"
    ):

        version()

        return True


    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    if lower in (
        "clear",
        "cls"
    ):

        clear_screen()

        return True


    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    if lower == "history":

        show_history()

        return True


    # --------------------------------------------------------
    # PWD
    # --------------------------------------------------------

    if lower == "pwd":

        show_pwd()

        return True


    # --------------------------------------------------------
    # WHOAMI
    # --------------------------------------------------------

    if lower == "whoami":

        show_user()

        return True


    # --------------------------------------------------------
    # CD
    # --------------------------------------------------------

    if (
        lower == "cd"
        or lower.startswith("cd ")
    ):

        change_directory(command)

        return True


    # --------------------------------------------------------
    # BASH
    # --------------------------------------------------------

    execute(command)

    return True


# ============================================================
#                           APP
# ============================================================

def run():

    if not check_environment():

        return 1

    banner()

    while True:

        try:

            command = input(
                prompt()
            ).strip()

        except KeyboardInterrupt:

            print()

            continue

        except EOFError:

            print()
            print(
                "Saliendo de Lysh..."
            )

            break


        if not command:

            continue


        command_history.append(
            command
        )


        if not process_command(
            command
        ):

            break


    return 0


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":

    sys.exit(
        run()
    )
