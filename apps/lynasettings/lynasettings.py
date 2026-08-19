#!/usr/bin/env python3

import os
import platform
import sys
from pathlib import Path


APP_NAME = "LynaSettings"
APP_VERSION = "0.3"

LYNAOS_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = LYNAOS_ROOT / "etc"
CONFIG_FILE = CONFIG_DIR / "lyna.conf"


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════╗
║        LynaSettings 0.3              ║
║       Configuración de LynaOS        ║
╚══════════════════════════════════════╝
""")


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print("""
LynaSettings 0.3

Comandos:

  INFO       Información del sistema
  CONFIG     Mostrar configuración
  SET        Cambiar una configuración
  RESET      Restaurar configuración
  PATH       Mostrar rutas de LynaOS
  CLEAR      Limpiar pantalla
  ABOUT      Información de LynaSettings
  H          Ayuda
  Q          Salir

Ejemplos:

  INFO
  CONFIG
  SET username Lyna
  PATH
""")


# ============================================================
#                    CONFIGURACIÓN PREDETERMINADA
# ============================================================

DEFAULT_CONFIG = {
    "username": "user",
    "language": "es",
    "theme": "default",
    "music_dir": "music",
}


# ============================================================
#                    LEER CONFIGURACIÓN
# ============================================================

def load_config():

    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    config = DEFAULT_CONFIG.copy()

    if not CONFIG_FILE.exists():

        save_config(config)

        return config

    try:

        with CONFIG_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split(
                    "=",
                    1
                )

                key = key.strip()
                value = value.strip()

                if key:

                    config[key] = value

    except Exception as error:

        print(
            f"Error leyendo configuración: {error}"
        )

    return config


# ============================================================
#                   GUARDAR CONFIGURACIÓN
# ============================================================

def save_config(config):

    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        with CONFIG_FILE.open(
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "# LynaOS configuration\n"
            )

            for key, value in config.items():

                file.write(
                    f"{key}={value}\n"
                )

        return True

    except Exception as error:

        print(
            f"Error guardando configuración: {error}"
        )

        return False


# ============================================================
#                    INFORMACIÓN DEL SISTEMA
# ============================================================

def system_info():

    print("""
╔══════════════════════════════════════╗
║          Información del sistema     ║
╚══════════════════════════════════════╝
""")

    print(
        f"Sistema:       {platform.system()}"
    )

    print(
        f"Plataforma:    {platform.platform()}"
    )

    print(
        f"Arquitectura:  {platform.machine()}"
    )

    print(
        f"Python:        {platform.python_version()}"
    )

    print(
        f"LynaOS:        0.3"
    )

    print(
        f"Directorio:    {LYNAOS_ROOT}"
    )

    print(
        f"Configuración: {CONFIG_FILE}"
    )


# ============================================================
#                       MOSTRAR CONFIG
# ============================================================

def show_config(config):

    print("""
╔══════════════════════════════════════╗
║           Configuración              ║
╚══════════════════════════════════════╝
""")

    for key, value in config.items():

        print(
            f"{key:<15} = {value}"
        )


# ============================================================
#                      CAMBIAR CONFIG
# ============================================================

def set_config(config, command):

    parts = command.split(
        None,
        2
    )

    if len(parts) < 3:

        print(
            "Uso: SET <opción> <valor>"
        )

        return

    key = parts[1]
    value = parts[2]

    if not key:

        print(
            "Opción inválida."
        )

        return

    config[key] = value

    if save_config(config):

        print(
            f"✓ {key} = {value}"
        )


# ============================================================
#                       RESTABLECER
# ============================================================

def reset_config(config):

    confirmation = input(
        "¿Restaurar configuración? [s/N]: "
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

    config.clear()

    config.update(
        DEFAULT_CONFIG
    )

    if save_config(config):

        print(
            "✓ Configuración restaurada."
        )


# ============================================================
#                           RUTAS
# ============================================================

def show_paths():

    print("""
╔══════════════════════════════════════╗
║             Rutas LynaOS             ║
╚══════════════════════════════════════╝
""")

    print(
        f"LynaOS:      {LYNAOS_ROOT}"
    )

    print(
        f"Aplicaciones:{LYNAOS_ROOT / 'apps'}"
    )

    print(
        f"Sistema:     {LYNAOS_ROOT / 'system'}"
    )

    print(
        f"Kernel:      {LYNAOS_ROOT / 'kernel'}"
    )

    print(
        f"Boot:        {LYNAOS_ROOT / 'boot'}"
    )

    print(
        f"Configuración: {CONFIG_DIR}"
    )

    print(
        f"Música:      {LYNAOS_ROOT / 'music'}"
    )


# ============================================================
#                           ABOUT
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Administrador de configuración
de LynaOS.

Funciones:

  • Información del sistema
  • Configuración persistente
  • Rutas del sistema
  • Restauración de configuración

Archivo:

  {CONFIG_FILE}
""")


# ============================================================
#                            APP
# ============================================================

def run():

    config = load_config()

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

        upper = command.upper()

        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        if upper in (
            "Q",
            "EXIT"
        ):

            print(
                "Saliendo de LynaSettings..."
            )

            break

        # ----------------------------------------------------
        # AYUDA
        # ----------------------------------------------------

        elif upper in (
            "H",
            "HELP"
        ):

            help_command()

        # ----------------------------------------------------
        # INFO
        # ----------------------------------------------------

        elif upper == "INFO":

            system_info()

        # ----------------------------------------------------
        # CONFIG
        # ----------------------------------------------------

        elif upper == "CONFIG":

            show_config(config)

        # ----------------------------------------------------
        # SET
        # ----------------------------------------------------

        elif upper.startswith("SET "):

            set_config(
                config,
                command
            )

        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        elif upper == "RESET":

            reset_config(config)

        # ----------------------------------------------------
        # PATH
        # ----------------------------------------------------

        elif upper == "PATH":

            show_paths()

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        elif upper == "CLEAR":

            os.system("clear")

        # ----------------------------------------------------
        # ABOUT
        # ----------------------------------------------------

        elif upper == "ABOUT":

            about()

        # ----------------------------------------------------
        # DESCONOCIDO
        # ----------------------------------------------------

        else:

            print(
                "Comando desconocido."
            )

            print(
                "Escribe H para ver la ayuda."
            )


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":
    run()
