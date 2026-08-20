#!/usr/bin/env python3

import json
import os
import platform
import shutil
import sys
from pathlib import Path


APP_NAME = "LynaSettings"
APP_VERSION = "0.4"

LYNAOS_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = LYNAOS_ROOT / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"


DEFAULT_SETTINGS = {
    "system": {
        "username": "Lyna",
        "language": "es",
        "theme": "default"
    },

    "lynafm": {
        "volume": 100,
        "autoplay": True
    },

    "lynatop": {
        "refresh": 2
    },

    "lysh": {
        "shell": "bash"
    },

    "lynastore": {
        "manager": "auto"
    }
}


settings = {}


# ============================================================
#                         UTILIDADES
# ============================================================

def clear():
    os.system("clear")


def deep_copy(data):
    return json.loads(json.dumps(data))


def merge_settings(defaults, current):
    """
    Conserva los valores existentes y añade automáticamente
    las nuevas opciones que aparezcan en versiones futuras.
    """

    result = deep_copy(defaults)

    if not isinstance(current, dict):
        return result

    for key, value in current.items():

        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):

            result[key] = merge_settings(
                result[key],
                value
            )

        else:

            result[key] = value

    return result


# ============================================================
#                       PERSISTENCIA
# ============================================================

def load_settings():

    global settings

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not SETTINGS_FILE.exists():

        settings = deep_copy(
            DEFAULT_SETTINGS
        )

        save_settings(
            silent=True
        )

        return

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        settings = merge_settings(
            DEFAULT_SETTINGS,
            data
        )

    except Exception as error:

        print(
            f"✗ Error leyendo configuración: {error}"
        )

        settings = deep_copy(
            DEFAULT_SETTINGS
        )


def save_settings(silent=False):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        temporary = SETTINGS_FILE.with_suffix(
            ".tmp"
        )

        with open(
            temporary,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                settings,
                file,
                ensure_ascii=False,
                indent=2
            )

        temporary.replace(
            SETTINGS_FILE
        )

        if not silent:

            print(
                "✓ Configuración guardada."
            )

        return True

    except Exception as error:

        print(
            f"✗ No se pudo guardar la configuración: {error}"
        )

        return False


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print(
        f"LynaSettings {APP_VERSION}"
    )

    print(
        "─" * 48
    )

    print(
        "Configuración de LynaOS"
    )

    print(
        "─" * 48
    )


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print("""
LynaSettings 0.4

Comandos:

  INFO              Información de LynaOS
  SYSTEM            Configuración del sistema
  FM                Configuración de LynaFM
  TOP               Configuración de LynaTop
  SHELL             Configuración de Lysh
  STORE             Configuración de LynaStore

  SAVE              Guardar configuración
  LOAD              Recargar configuración
  RESET             Restablecer configuración

  CLEAR             Limpiar pantalla
  HELP              Ayuda
  Q                 Salir

Configuración:

  SYSTEM USERNAME   Cambiar nombre de usuario
  SYSTEM LANGUAGE   Cambiar idioma
  SYSTEM THEME      Cambiar tema

  FM VOLUME         Cambiar volumen
  FM AUTOPLAY       Activar/desactivar reproducción automática

  TOP REFRESH       Cambiar intervalo de actualización

  SHELL SHELL       Cambiar shell utilizada

  STORE MANAGER     Elegir gestor de paquetes

Ejemplos:

  SYSTEM USERNAME Lyna
  SYSTEM LANGUAGE es
  SYSTEM THEME default

  FM VOLUME 80
  FM AUTOPLAY ON

  TOP REFRESH 3

  SHELL SHELL bash

  STORE MANAGER auto

  SAVE
""")


# ============================================================
#                           INFO
# ============================================================

def system_info():

    print("""
╔══════════════════════════════════════╗
║          Información LynaOS          ║
╚══════════════════════════════════════╝
""")

    print(
        f"Sistema:          LynaOS"
    )

    print(
        f"LynaSettings:     {APP_VERSION}"
    )

    print(
        f"Python:           {sys.version.split()[0]}"
    )

    print(
        f"Plataforma:       {platform.system()}"
    )

    print(
        f"Arquitectura:     {platform.machine()}"
    )

    print(
        f"Directorio:       {LYNAOS_ROOT}"
    )

    print(
        f"Configuración:    {SETTINGS_FILE}"
    )

    print(
        f"pkg disponible:   {'Sí' if shutil.which('pkg') else 'No'}"
    )

    print(
        f"apt disponible:   {'Sí' if shutil.which('apt') else 'No'}"
    )

    print(
        f"bash disponible:  {'Sí' if shutil.which('bash') else 'No'}"
    )


# ============================================================
#                       MOSTRAR SECCIÓN
# ============================================================

def show_section(section):

    data = settings.get(
        section
    )

    if not isinstance(data, dict):

        print(
            "Sección inexistente."
        )

        return

    print()
    print(
        f"╔══ {section.upper()} ══╗"
    )

    for key, value in data.items():

        if isinstance(value, bool):

            value = (
                "ON"
                if value
                else "OFF"
            )

        print(
            f"{key:<12} = {value}"
        )

    print()


# ============================================================
#                       CONVERTIR VALOR
# ============================================================

def parse_value(value):

    upper = value.upper()

    if upper in (
        "ON",
        "TRUE",
        "YES",
        "SI",
        "SÍ"
    ):

        return True

    if upper in (
        "OFF",
        "FALSE",
        "NO"
    ):

        return False

    try:

        if "." in value:

            return float(value)

        return int(value)

    except ValueError:

        return value


# ============================================================
#                     CAMBIAR CONFIGURACIÓN
# ============================================================

def set_setting(section, key, value):

    section_data = settings.get(
        section
    )

    if not isinstance(section_data, dict):

        print(
            "✗ Sección inexistente."
        )

        return

    if key not in section_data:

        print(
            f"✗ Opción inexistente: {key}"
        )

        return

    new_value = parse_value(
        value
    )

    # --------------------------------------------
    # VALIDACIONES
    # --------------------------------------------

    if section == "lynafm":

        if key == "volume":

            if not isinstance(
                new_value,
                (int, float)
            ):

                print(
                    "✗ El volumen debe ser un número."
                )

                return

            if not 0 <= new_value <= 100:

                print(
                    "✗ El volumen debe estar entre 0 y 100."
                )

                return

    if section == "lynatop":

        if key == "refresh":

            if not isinstance(
                new_value,
                (int, float)
            ):

                print(
                    "✗ El intervalo debe ser un número."
                )

                return

            if new_value <= 0:

                print(
                    "✗ El intervalo debe ser mayor que 0."
                )

                return

    if section == "lynastore":

        if key == "manager":

            allowed = (
                "auto",
                "pkg",
                "apt"
            )

            if str(new_value).lower() not in allowed:

                print(
                    "✗ Usa: auto, pkg o apt."
                )

                return

            new_value = str(
                new_value
            ).lower()

    if section == "lysh":

        if key == "shell":

            new_value = str(
                new_value
            )

    section_data[key] = new_value

    save_settings()

    print(
        f"✓ {section}.{key} = {new_value}"
    )


# ============================================================
#                        SYSTEM
# ============================================================

def system_command(parts):

    if len(parts) == 1:

        show_section(
            "system"
        )

        return

    key = parts[1].lower()

    if len(parts) < 3:

        print(
            f"Valor actual: {settings['system'].get(key, '?')}"
        )

        return

    value = " ".join(
        parts[2:]
    )

    set_setting(
        "system",
        key,
        value
    )


# ============================================================
#                           FM
# ============================================================

def fm_command(parts):

    if len(parts) == 1:

        show_section(
            "lynafm"
        )

        return

    key = parts[1].lower()

    if len(parts) < 3:

        print(
            f"Valor actual: {settings['lynafm'].get(key, '?')}"
        )

        return

    value = " ".join(
        parts[2:]
    )

    set_setting(
        "lynafm",
        key,
        value
    )


# ============================================================
#                           TOP
# ============================================================

def top_command(parts):

    if len(parts) == 1:

        show_section(
            "lynatop"
        )

        return

    key = parts[1].lower()

    if len(parts) < 3:

        print(
            f"Valor actual: {settings['lynatop'].get(key, '?')}"
        )

        return

    value = " ".join(
        parts[2:]
    )

    set_setting(
        "lynatop",
        key,
        value
    )


# ============================================================
#                          SHELL
# ============================================================

def shell_command(parts):

    if len(parts) == 1:

        show_section(
            "lysh"
        )

        return

    key = parts[1].lower()

    if len(parts) < 3:

        print(
            f"Valor actual: {settings['lysh'].get(key, '?')}"
        )

        return

    value = " ".join(
        parts[2:]
    )

    set_setting(
        "lysh",
        key,
        value
    )


# ============================================================
#                         STORE
# ============================================================

def store_command(parts):

    if len(parts) == 1:

        show_section(
            "lynastore"
        )

        return

    key = parts[1].lower()

    if len(parts) < 3:

        print(
            f"Valor actual: {settings['lynastore'].get(key, '?')}"
        )

        return

    value = " ".join(
        parts[2:]
    )

    set_setting(
        "lynastore",
        key,
        value
    )


# ============================================================
#                          RESET
# ============================================================

def reset_settings():

    print()
    print(
        "⚠ Esto restablecerá toda la configuración."
    )

    confirmation = input(
        "¿Continuar? [s/N]: "
    ).strip().lower()

    if confirmation not in (
        "s",
        "si",
        "sí",
        "y",
        "yes"
    ):

        print(
            "Operación cancelada."
        )

        return

    global settings

    settings = deep_copy(
        DEFAULT_SETTINGS
    )

    save_settings()

    print(
        "✓ Configuración restablecida."
    )


# ============================================================
#                           APP
# ============================================================

def run():

    load_settings()

    clear()
    banner()

    while True:

        try:

            command = input(
                "lynasettings> "
            ).strip()

        except KeyboardInterrupt:

            print()
            print(
                "Saliendo de LynaSettings..."
            )

            break

        except EOFError:

            print()

            break

        if not command:
            continue

        parts = command.split()

        action = parts[0].upper()

        # --------------------------------------------
        # SALIR
        # --------------------------------------------

        if action in (
            "Q",
            "EXIT"
        ):

            print(
                "Saliendo de LynaSettings..."
            )

            break

        # --------------------------------------------
        # AYUDA
        # --------------------------------------------

        elif action in (
            "H",
            "HELP"
        ):

            help_command()

        # --------------------------------------------
        # INFO
        # --------------------------------------------

        elif action == "INFO":

            system_info()

        # --------------------------------------------
        # SYSTEM
        # --------------------------------------------

        elif action == "SYSTEM":

            system_command(
                parts
            )

        # --------------------------------------------
        # FM
        # --------------------------------------------

        elif action == "FM":

            fm_command(
                parts
            )

        # --------------------------------------------
        # TOP
        # --------------------------------------------

        elif action == "TOP":

            top_command(
                parts
            )

        # --------------------------------------------
        # SHELL
        # --------------------------------------------

        elif action == "SHELL":

            shell_command(
                parts
            )

        # --------------------------------------------
        # STORE
        # --------------------------------------------

        elif action == "STORE":

            store_command(
                parts
            )

        # --------------------------------------------
        # SAVE
        # --------------------------------------------

        elif action == "SAVE":

            save_settings()

        # --------------------------------------------
        # LOAD
        # --------------------------------------------

        elif action == "LOAD":

            load_settings()

            print(
                "✓ Configuración recargada."
            )

        # --------------------------------------------
        # RESET
        # --------------------------------------------

        elif action == "RESET":

            reset_settings()

        # --------------------------------------------
        # CLEAR
        # --------------------------------------------

        elif action == "CLEAR":

            clear()
            banner()

        # --------------------------------------------
        # DESCONOCIDO
        # --------------------------------------------

        else:

            print(
                "Comando desconocido."
            )

            print(
                "Escribe HELP para ver los comandos."
            )


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":
    run()
