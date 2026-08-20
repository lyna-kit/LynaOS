#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


# ============================================================
#                         LynaOS 0.4
# ============================================================

APP_NAME = "LynaOS"
VERSION = "0.4"

ROOT = Path(__file__).resolve().parent
APPS_DIR = ROOT / "apps"


# ============================================================
#                       APLICACIONES
# ============================================================

APPLICATIONS = {
    "1": ("LynaCalc", "lynacalc", "lynacalc.py"),
    "2": ("LynaFiles", "lynafiles", "lynafiles.py"),
    "3": ("LynaFM", "lynafm", "lynafm.py"),
    "4": ("LynaSettings", "lynasettings", "lynasettings.py"),
    "5": ("LynaStore", "lynastore", "lynastore.py"),
    "6": ("Shelly", "shelly", "shelly.py"),
    "7": ("LynaClock", "lynaclock", "lynaclock.py"),
    "8": ("LynaTop", "lynatop", "lynatop.py"),
    "9": ("Lysh", "lysh", "lysh.py"),
}


# ============================================================
#                           BANNER
# ============================================================

def banner():

    os.system("clear")

    print("""
╔══════════════════════════════════════╗
║             LynaOS 0.4               ║
║       Sistema operativo LynaOS       ║
╚══════════════════════════════════════╝
""")


# ============================================================
#                           MENÚ
# ============================================================

def menu():

    print("Aplicaciones:")
    print()

    for key, application in APPLICATIONS.items():

        name = application[0]

        print(
            f"  {key}. {name}"
        )

    print()
    print("Sistema:")
    print()
    print("  I. Información")
    print("  B. LynaBash")
    print("  R. Reiniciar")
    print("  Q. Salir")
    print()


# ============================================================
#                       INFORMACIÓN
# ============================================================

def system_info():

    print("""
╔══════════════════════════════════════╗
║          Información LynaOS          ║
╚══════════════════════════════════════╝
""")

    print(
        f"Sistema:       {APP_NAME}"
    )

    print(
        f"Versión:       {VERSION}"
    )

    print(
        f"Directorio:    {ROOT}"
    )

    print(
        f"Aplicaciones:  {len(APPLICATIONS)}"
    )

    print(
        f"Python:        {sys.version.split()[0]}"
    )

    print()
    print("Aplicaciones LynaOS 0.4:")
    print()

    for key, application in APPLICATIONS.items():

        name, directory, filename = application

        app_path = (
            APPS_DIR /
            directory /
            filename
        )

        status = (
            "✓"
            if app_path.exists()
            else "✗"
        )

        print(
            f"  {status} {name}"
        )

    print()
    print("LynaBash: Bash para LynaOS")
    print("Lysh: Terminal Bash en Python")
    print("LynaTop: Monitor basado en /proc")


# ============================================================
#                 COMPROBAR APLICACIÓN
# ============================================================

def application_exists(
    directory,
    filename
):

    app_path = (
        APPS_DIR /
        directory /
        filename
    )

    return app_path.exists()


# ============================================================
#                     EJECUTAR APLICACIÓN
# ============================================================

def launch_application(key):

    if key not in APPLICATIONS:

        print(
            "LynaOS: aplicación no encontrada."
        )

        return

    name, directory, filename = (
        APPLICATIONS[key]
    )

    app_path = (
        APPS_DIR /
        directory /
        filename
    )

    if not application_exists(
        directory,
        filename
    ):

        print()
        print(
            f"✗ {name} no está instalada correctamente."
        )

        print(
            f"Falta: {app_path}"
        )

        return

    print()
    print(
        f"▶ Iniciando {name}..."
    )
    print()

    try:

        subprocess.run(
            [
                sys.executable,
                str(app_path)
            ]
        )

    except KeyboardInterrupt:

        print()

    except Exception as error:

        print(
            f"LynaOS: error ejecutando {name}:"
        )

        print(error)

    input(
        "\nPresiona ENTER para volver a LynaOS..."
    )


# ============================================================
#                       LYNABASH
# ============================================================

def launch_bash():

    bash = (
        ROOT /
        "shell" /
        "lynashell.sh"
    )

    if not bash.exists():

        print()
        print(
            "✗ LynaBash no está instalado."
        )

        print(
            f"Falta: {bash}"
        )

        input(
            "\nPresiona ENTER para continuar..."
        )

        return

    print()
    print(
        "▶ Iniciando LynaBash..."
    )
    print()

    try:

        subprocess.run(
            [
                "bash",
                str(bash)
            ]
        )

    except KeyboardInterrupt:

        print()

    except Exception as error:

        print(
            f"LynaOS: error iniciando LynaBash:"
        )

        print(error)

    input(
        "\nPresiona ENTER para volver a LynaOS..."
    )


# ============================================================
#                       REINICIAR
# ============================================================

def restart():

    print()
    print(
        "Reiniciando LynaOS..."
    )

    main()


# ============================================================
#                       APAGAR
# ============================================================

def shutdown():

    print()
    print(
        "Apagando LynaOS..."
    )


# ============================================================
                            MAIN
# ============================================================

def main():

    while True:

        banner()
        menu()

        try:

            command = input(
                "lynaos> "
            ).strip()

        except KeyboardInterrupt:

            print()
            shutdown()

            break

        except EOFError:

            print()
            shutdown()

            break

        if not command:

            continue

        command = command.upper()

        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        if command in (
            "Q",
            "EXIT",
            "QUIT"
        ):

            shutdown()

            break

        # ----------------------------------------------------
        # INFORMACIÓN
        # ----------------------------------------------------

        elif command in (
            "I",
            "INFO",
            "ABOUT"
        ):

            system_info()

            input(
                "\nPresiona ENTER para continuar..."
            )

        # ----------------------------------------------------
        # LYNABASH
        # ----------------------------------------------------

        elif command in (
            "B",
            "BASH",
            "LYNABASH"
        ):

            launch_bash()

        # ----------------------------------------------------
        # REINICIAR
        # ----------------------------------------------------

        elif command in (
            "R",
            "RESTART",
            "REBOOT"
        ):

            continue

        # ----------------------------------------------------
        # APLICACIONES
        # ----------------------------------------------------

        elif command in APPLICATIONS:

            launch_application(
                command
            )

        # ----------------------------------------------------
        # LYSH DIRECTO
        # ----------------------------------------------------

        elif command in (
            "LYSH",
            "SHELL"
        ):

            launch_application(
                "9"
            )

        # ----------------------------------------------------
        # AYUDA
        # ----------------------------------------------------

        elif command in (
            "H",
            "HELP",
            "?"
        ):

            print()
            print(
                "Introduce el número de una aplicación."
            )

            print(
                "I = Información"
            )

            print(
                "B = LynaBash"
            )

            print(
                "R = Reiniciar"
            )

            print(
                "Q = Salir"
            )

            input(
                "\nPresiona ENTER para continuar..."
            )

        # ----------------------------------------------------
        # COMANDO DESCONOCIDO
        # ----------------------------------------------------

        else:

            print()
            print(
                "Comando desconocido."
            )

            print(
                "Escribe H para ver la ayuda."
            )

            input(
                "\nPresiona ENTER para continuar..."
            )


# ============================================================
#                            START
# ============================================================

if __name__ == "__main__":

    main()
