#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys


APP_NAME = "Lysh"
APP_VERSION = "0.1"

BASH = shutil.which("bash")


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════════════════════════╗
║                       Lysh 0.1                          ║
║                LynaOS Shell Interface                   ║
╚══════════════════════════════════════════════════════════╝

Lysh utiliza Bash de Termux.

Escribe 'exit' para volver a LynaOS.
Escribe 'help' para ver información.
""")


# ============================================================
#                       COMPROBAR BASH
# ============================================================

def check_bash():

    if BASH is None:

        print("✗ Bash no está disponible.")

        print()
        print(
            "En Termux puedes instalarlo con:"
        )

        print(
            "pkg install bash"
        )

        return False

    return True


# ============================================================
#                         AYUDA
# ============================================================

def help_command():

    print("""
Lysh 0.1

Lysh es la interfaz de shell de LynaOS.

El shell utilizado es Bash.

Comandos especiales:

  help       Mostrar esta ayuda
  version    Mostrar versión
  clear      Limpiar pantalla
  exit       Salir de Lysh

Todos los demás comandos se ejecutan
directamente mediante Bash.

Ejemplos:

  ls
  pwd
  cd ..
  mkdir prueba
  chmod +x archivo.sh
  ./archivo.sh
  python programa.py
  git status
""")


# ============================================================
#                         VERSION
# ============================================================

def version():

    print(
        f"{APP_NAME} {APP_VERSION}"
    )

    print(
        "Bash backend:"
    )

    print(
        BASH if BASH else "No disponible"
    )


# ============================================================
#                    EJECUTAR COMANDO
# ============================================================

def execute(command):

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

    except Exception as error:

        print(
            f"Lysh: error: {error}"
        )

        return 1


# ============================================================
#                         PROMPT
# ============================================================

def prompt():

    current_directory = os.getcwd()

    home = os.path.expanduser("~")

    if current_directory.startswith(home):

        current_directory = (
            "~" +
            current_directory[
                len(home):
            ]
        )

    return (
        f"\033[32m"
        f"lysh"
        f"\033[0m:"
        f"\033[34m"
        f"{current_directory}"
        f"\033[0m$ "
    )


# ============================================================
#                           APP
# ============================================================

def run():

    if not check_bash():

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

            break


        if not command:

            continue


        lower = command.lower()


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if lower in (
            "exit",
            "quit"
        ):

            print(
                "Saliendo de Lysh..."
            )

            break


        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        if lower == "help":

            help_command()

            continue


        # ----------------------------------------------------
        # VERSION
        # ----------------------------------------------------

        if lower in (
            "version",
            "--version"
        ):

            version()

            continue


        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        if lower == "clear":

            os.system("clear")

            continue


        # ----------------------------------------------------
        # BASH
        # ----------------------------------------------------

        execute(command)


    return 0


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":

    sys.exit(
        run()
    )
