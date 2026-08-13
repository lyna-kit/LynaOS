#!/usr/bin/env python3

import os
import sys
import json
import shlex
import shutil
import subprocess
from pathlib import Path


# ============================================================
#                         LynaOS 0.2
# ============================================================

LYNAOS_NAME = "LynaOS"
LYNAOS_VERSION = "0.2"

LYNAOS_ROOT = Path(__file__).resolve().parent
APPS_DIR = LYNAOS_ROOT / "apps"
CONFIG_DIR = Path.home() / ".lynaos"
CONFIG_FILE = CONFIG_DIR / "config.json"


# ============================================================
#                       CONFIGURACIÓN
# ============================================================

DEFAULT_CONFIG = {
    "name": "LynaOS",
    "version": LYNAOS_VERSION,
    "user": "lyna",
    "hostname": "lynaos",
    "theme": "default",
    "language": "es",
    "music": True,
    "notifications": True
}


def load_config():

    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not CONFIG_FILE.exists():

        save_config(
            DEFAULT_CONFIG.copy()
        )

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return DEFAULT_CONFIG.copy()


def save_config(config):

    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            config,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
#                        BANNER
# ============================================================

def banner():

    config = load_config()

    print("""
╔══════════════════════════════════════════╗
║                                          ║
║                 LynaOS                   ║
║                  0.2                     ║
║                                          ║
║        Lightweight OS for Termux         ║
║                                          ║
╚══════════════════════════════════════════╝
""")

    print(
        f"Bienvenida, {config.get('user', 'lyna')}."
    )

    print(
        "Escribe 'help' para obtener ayuda."
    )

    print()


# ============================================================
#                       APLICACIONES
# ============================================================

def get_apps():

    apps = {}

    if not APPS_DIR.exists():

        return apps

    for directory in sorted(
        APPS_DIR.iterdir()
    ):

        if not directory.is_dir():
            continue

        python_files = list(
            directory.glob("*.py")
        )

        if not python_files:
            continue

        main_file = None

        preferred = (
            directory.name
            + ".py"
        )

        for file in python_files:

            if file.name == preferred:

                main_file = file
                break

        if main_file is None:

            main_file = python_files[0]

        command = directory.name.lower()

        apps[command] = main_file

    return apps


def list_apps():

    apps = get_apps()

    print("""
Aplicaciones disponibles
────────────────────────
""")

    if not apps:

        print(
            "No hay aplicaciones instaladas."
        )

        return

    for command, path in apps.items():

        print(
            f"  ✓ {command}"
        )


def launch_app(command, args=None):

    if args is None:
        args = []

    apps = get_apps()

    command = command.lower()

    if command not in apps:

        return False

    application = apps[command]

    try:

        result = subprocess.run(
            [
                sys.executable,
                str(application),
                *args
            ]
        )

        return True

    except KeyboardInterrupt:

        return True

    except Exception as error:

        print(
            f"LynaOS: error ejecutando {command}: {error}"
        )

        return True


# ============================================================
#                          INFO
# ============================================================

def system_info():

    config = load_config()

    print(f"""
{LYNAOS_NAME} {LYNAOS_VERSION}

Sistema operativo : {LYNAOS_NAME}
Versión           : {LYNAOS_VERSION}
Usuario           : {config.get("user")}
Hostname          : {config.get("hostname")}
Arquitectura     : {os.uname().machine}
Directorio       : {LYNAOS_ROOT}
Aplicaciones     : {len(get_apps())}
""")


# ============================================================
#                           HELP
# ============================================================

def help_command():

    print("""
╔══════════════════════════════════════════╗
║              LynaOS 0.2                  ║
╚══════════════════════════════════════════╝

Comandos del sistema:

  help              Mostrar esta ayuda
  apps              Mostrar aplicaciones
  about             Información del sistema
  clear             Limpiar pantalla
  exit              Apagar LynaOS

Aplicaciones:

  lynacalc          Calculadora
  lynafiles         Gestor de archivos
  lynasettings      Ajustes
  lynastore         Tienda de aplicaciones
  lynafm            Reproductor de música
  shelly            Navegador de texto

También puedes ejecutar comandos normales
de Termux mediante LynaBash.
""")


# ============================================================
#                       COMANDOS LINUX
# ============================================================

def execute_shell(command):

    try:

        arguments = shlex.split(
            command
        )

        if not arguments:
            return

        subprocess.run(
            arguments
        )

    except FileNotFoundError:

        print(
            f"Comando no encontrado: {arguments[0]}"
        )

    except Exception as error:

        print(
            f"LynaBash: {error}"
        )


# ============================================================
#                       LynaBash
# ============================================================

def shell():

    while True:

        config = load_config()

        prompt = (
            f"{config.get('user', 'lyna')}"
            "@"
            f"{config.get('hostname', 'lynaos')}"
            ":~$ "
        )

        try:

            command = input(
                prompt
            ).strip()

            if not command:
                continue

            parts = shlex.split(
                command
            )

            cmd = parts[0].lower()

            args = parts[1:]

            # ------------------------------------------------
            # SISTEMA
            # ------------------------------------------------

            if cmd == "help":

                help_command()

            elif cmd == "apps":

                list_apps()

            elif cmd in (
                "about",
                "neofetch",
                "info"
            ):

                system_info()

            elif cmd == "clear":

                os.system("clear")

            elif cmd in (
                "exit",
                "shutdown"
            ):

                print(
                    "\nApagando LynaOS..."
                )

                break

            # ------------------------------------------------
            # APLICACIONES
            # ------------------------------------------------

            elif launch_app(
                cmd,
                args
            ):

                pass

            # ------------------------------------------------
            # BASH / TERMUX
            # ------------------------------------------------

            else:

                execute_shell(
                    command
                )

        except KeyboardInterrupt:

            print()

        except EOFError:

            print()

            break


# ============================================================
#                         ARRANQUE
# ============================================================

def boot():

    os.system("clear")

    banner()

    print(
        "Inicializando LynaOS..."
    )

    print(
        f"Aplicaciones detectadas: {len(get_apps())}"
    )

    print(
        "LynaBash iniciado.\n"
    )

    shell()


# ============================================================
#                           MAIN
# ============================================================

def main():

    if len(sys.argv) > 1:

        argument = sys.argv[1]

        if argument in (
            "--version",
            "-v"
        ):

            print(
                f"{LYNAOS_NAME} {LYNAOS_VERSION}"
            )

            return

        if argument in (
            "--apps",
            "-a"
        ):

            list_apps()

            return

        if argument in (
            "--info",
            "-i"
        ):

            system_info()

            return

    boot()


if __name__ == "__main__":

    main()
