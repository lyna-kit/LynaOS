#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


# ============================================================
#                         LynaOS 0.3.1
# ============================================================

APP_NAME = "LynaOS"
VERSION = "0.3.1"

ROOT = Path(__file__).resolve().parent
APPS_DIR = ROOT / "apps"


# ============================================================
#                         APLICACIONES
# ============================================================

APPLICATIONS = {
    "1": ("LynaCalc", "lynacalc", "main.py"),
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
║           LynaOS 0.3.1               ║
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

    print(f"""
╔══════════════════════════════════════╗
║          Información LynaOS          ║
╚══════════════════════════════════════╝

Sistema:       {APP_NAME}
Versión:       {VERSION}
Directorio:    {ROOT}
Aplicaciones:  {len(APPLICATIONS)}

Python:        {sys.version.split()[0]}

Nuevas herramientas:

  LynaTop       0.3.1
  Lysh          0.1

Lysh utiliza Bash de Termux.
LynaTop funciona sin psutil.
""")


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

    if not app_path.exists():

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
#                         LYSH
# ============================================================

def launch_lysh():

    lysh = (
        APPS_DIR /
        "lysh" /
        "lysh.py"
    )

    if not lysh.exists():

        print()
        print(
            "✗ Lysh no está instalado correctamente."
        )

        print(
            f"Falta: {lysh}"
        )

        return

    print()
    print(
        "▶ Iniciando Lysh..."
    )
    print()

    try:

        subprocess.run(
            [
                sys.executable,
                str(lysh)
            ]
        )

    except KeyboardInterrupt:

        print()

    except Exception as error:

        print(
            f"LynaOS: error iniciando Lysh:"
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

        print(
            "LynaBash no está instalado."
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

    except Exception as error:

        print(
            f"Error iniciando LynaBash: {error}"
        )

    input(
        "\nPresiona ENTER para volver..."
    )


# ============================================================
#                       REINICIAR
# ============================================================

def restart():

    main()


# ============================================================
#                            MAIN
# ============================================================

def main():

    while True:

        banner()
        menu()

        command = input(
            "lynaos> "
        ).strip()

        if not command:

            continue

        command = command.upper()

        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        if command in (
            "Q",
            "EXIT"
        ):

            print()
            print(
                "Apagando LynaOS..."
            )

            break

        # ----------------------------------------------------
        # INFORMACIÓN
        # ----------------------------------------------------

        elif command == "I":

            system_info()

            input(
                "\nPresiona ENTER para continuar..."
            )

        # ----------------------------------------------------
        # LYNABASH
        # ----------------------------------------------------

        elif command == "B":

            launch_bash()

        # ----------------------------------------------------
        # REINICIAR
        # ----------------------------------------------------

        elif command == "R":

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

        elif command == "LYSH":

            launch_lysh()

        # ----------------------------------------------------
        # COMANDO DESCONOCIDO
        # ----------------------------------------------------

        else:

            print()
            print(
                "Comando desconocido."
            )

            input(
                "\nPresiona ENTER para continuar..."
            )


# ============================================================
#                            START
# ============================================================

if __name__ == "__main__":

    main()
