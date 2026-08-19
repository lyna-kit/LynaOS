#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


# ============================================================
#                         LynaOS 0.3
# ============================================================

APP_NAME = "LynaOS"
VERSION = "0.3"

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
}


# ============================================================
#                           BANNER
# ============================================================

def banner():

    os.system("clear")

    print("""
╔══════════════════════════════════════╗
║             LynaOS 0.3               ║
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

Sistema:       LynaOS
Versión:       {VERSION}
Directorio:    {ROOT}
Aplicaciones:  {len(APPLICATIONS)}

Python:        {sys.version.split()[0]}
""")


# ============================================================
#                     EJECUTAR APLICACIÓN
# ============================================================

def launch_application(key):

    if key not in APPLICATIONS:

        print(
            "LynaOS: aplicación no encontrada."
        )

        return

    name, directory, filename = APPLICATIONS[key]

    app_path = APPS_DIR / directory / filename

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
#                       LYNABASH
# ============================================================

def launch_bash():

    bash = ROOT / "shell" / "lynashell.sh"

    if not bash.exists():

        print(
            "LynaBash no está instalado."
        )

        return

    print()
    print("▶ Iniciando LynaBash...")
    print()

    try:

        subprocess.run(
            ["bash", str(bash)]
        )

    except Exception as error:

        print(
            f"Error iniciando LynaBash: {error}"
        )

    input(
        "\nPresiona ENTER para volver..."
    )


# ============================================================
#                         REINICIAR
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

        # --------------------------------------------
        # SALIR
        # --------------------------------------------

        if command in ("Q", "EXIT"):

            print()
            print(
                "Apagando LynaOS..."
            )

            break

        # --------------------------------------------
        # INFORMACIÓN
        # --------------------------------------------

        elif command == "I":

            system_info()

            input(
                "\nPresiona ENTER para continuar..."
            )

        # --------------------------------------------
        # LYNABASH
        # --------------------------------------------

        elif command == "B":

            launch_bash()

        # --------------------------------------------
        # REINICIAR
        # --------------------------------------------

        elif command == "R":

            continue

        # --------------------------------------------
        # APLICACIONES
        # --------------------------------------------

        elif command in APPLICATIONS:

            launch_application(command)

        # --------------------------------------------
        # COMANDO DESCONOCIDO
        # --------------------------------------------

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
