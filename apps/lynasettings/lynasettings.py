#!/usr/bin/env python3

import json
import os
from pathlib import Path


APP_NAME = "LynaSettings"
APP_VERSION = "0.1"

LYNAOS_DIR = Path.home() / ".lynaos"
CONFIG_FILE = LYNAOS_DIR / "config.json"


# ============================================================
#                         CONFIGURACIÓN
# ============================================================

DEFAULT_CONFIG = {
    "name": "LynaOS",
    "version": "0.1",
    "user": "lyna",
    "hostname": "lynaos",
    "theme": "default",
    "language": "es",
    "music": True,
    "notifications": True
}


def load_config():

    LYNAOS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not CONFIG_FILE.exists():

        save_config(DEFAULT_CONFIG.copy())

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

    LYNAOS_DIR.mkdir(
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
#                            ABOUT
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Centro de configuración de LynaOS.

Sistema: LynaOS
Versión: {APP_VERSION}
""")


# ============================================================
#                       MOSTRAR AJUSTES
# ============================================================

def show_settings():

    config = load_config()

    print("""
╔══════════════════════════════════════╗
║          AJUSTES DE LynaOS           ║
╚══════════════════════════════════════╝
""")

    print(
        f"1. Nombre       : {config.get('name')}"
    )

    print(
        f"2. Usuario      : {config.get('user')}"
    )

    print(
        f"3. Hostname     : {config.get('hostname')}"
    )

    print(
        f"4. Tema         : {config.get('theme')}"
    )

    print(
        f"5. Idioma       : {config.get('language')}"
    )

    print(
        f"6. Música       : {'Activada' if config.get('music') else 'Desactivada'}"
    )

    print(
        f"7. Notificaciones: {'Activadas' if config.get('notifications') else 'Desactivadas'}"
    )


# ============================================================
#                        CAMBIAR VALOR
# ============================================================

def change_setting():

    config = load_config()

    show_settings()

    print()
    print("Escribe el número del ajuste.")
    print("Escribe 'cancel' para cancelar.")

    choice = input(
        "Ajuste> "
    ).strip()

    if choice == "cancel":

        return

    if choice == "1":

        value = input(
            "Nuevo nombre de LynaOS: "
        ).strip()

        if value:
            config["name"] = value

    elif choice == "2":

        value = input(
            "Nuevo usuario: "
        ).strip()

        if value:
            config["user"] = value

    elif choice == "3":

        value = input(
            "Nuevo hostname: "
        ).strip()

        if value:
            config["hostname"] = value

    elif choice == "4":

        print()
        print("Temas disponibles:")
        print("  default")
        print("  dark")
        print("  light")

        value = input(
            "Tema> "
        ).strip().lower()

        if value in (
            "default",
            "dark",
            "light"
        ):

            config["theme"] = value

        else:

            print(
                "Tema no válido."
            )

            return

    elif choice == "5":

        print()
        print("Idiomas disponibles:")
        print("  es")
        print("  en")

        value = input(
            "Idioma> "
        ).strip().lower()

        if value in (
            "es",
            "en"
        ):

            config["language"] = value

        else:

            print(
                "Idioma no válido."
            )

            return

    elif choice == "6":

        config["music"] = not config.get(
            "music",
            True
        )

    elif choice == "7":

        config["notifications"] = not config.get(
            "notifications",
            True
        )

    else:

        print(
            "Opción no válida."
        )

        return

    save_config(config)

    print(
        "✓ Ajustes guardados."
    )


# ============================================================
#                         RESTABLECER
# ============================================================

def reset_settings():

    confirm = input(
        "¿Restablecer todos los ajustes? [s/N] "
    ).strip().lower()

    if confirm != "s":

        print(
            "Operación cancelada."
        )

        return

    save_config(
        DEFAULT_CONFIG.copy()
    )

    print(
        "✓ Ajustes restablecidos."
    )


# ============================================================
#                            AYUDA
# ============================================================

def help_command():

    print("""
LynaSettings 0.1

Comandos:

  settings    Ver configuración
  change      Cambiar configuración
  reset       Restablecer configuración
  about       Información
  clear       Limpiar pantalla
  help        Ayuda
  exit        Salir
""")


# ============================================================
#                          APLICACIÓN
# ============================================================

def run():

    print(f"""
╔══════════════════════════════════╗
║       {APP_NAME} {APP_VERSION}       ║
║       Ajustes de LynaOS         ║
╚══════════════════════════════════╝

Escribe 'help' para obtener ayuda.
""")

    while True:

        try:

            command = input(
                "lynasettings> "
            ).strip().lower()

            if not command:
                continue

            if command == "exit":
                break

            elif command == "help":
                help_command()

            elif command == "settings":
                show_settings()

            elif command == "change":
                change_setting()

            elif command == "reset":
                reset_settings()

            elif command == "about":
                about()

            elif command == "clear":
                os.system("clear")

            else:

                print(
                    f"LynaSettings: comando desconocido: {command}"
                )

        except KeyboardInterrupt:

            print()

        except EOFError:

            break


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":
    run()
