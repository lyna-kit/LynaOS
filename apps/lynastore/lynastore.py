#!/usr/bin/env python3

import os
import shutil
import subprocess


APP_NAME = "LynaStore"
APP_VERSION = "0.4"


# ============================================================
#                         UTILIDADES
# ============================================================

def command_exists(command):

    return shutil.which(command) is not None


def run_command(command):

    try:

        return subprocess.run(
            command,
            check=False
        )

    except KeyboardInterrupt:

        print()
        print("Operación cancelada.")

        return None

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )

        return None


def confirm(message):

    answer = input(
        f"{message} [s/N]: "
    ).strip().lower()

    return answer in (
        "s",
        "si",
        "sí",
        "y",
        "yes"
    )


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print(f"""
╔══════════════════════════════════════╗
║          LynaStore {APP_VERSION}             ║
║       Gestor de paquetes LynaOS      ║
╚══════════════════════════════════════╝

Compatible con:

  • pkg
  • apt
  • Python / pip
""")


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print(f"""
LynaStore {APP_VERSION}

Gestión de paquetes:

  I <paquete>       Instalar automáticamente
  U <paquete>       Desinstalar paquete
  S <paquete>       Buscar paquete

  P <paquete>       Instalar mediante pkg
  A <paquete>       Instalar mediante apt

Python:

  PY <paquete>      Instalar paquete con pip
  PYU               Actualizar paquetes de pip

Sistema:

  UPDATE            Actualizar índices
  UPGRADE           Actualizar paquetes
  SYSUP             Actualizar todo

Información:

  INFO              Información del sistema
  CLEAR             Limpiar pantalla
  H                 Ayuda
  Q                 Salir


Ejemplos:

  S python
  I python
  P git
  A curl

  PY requests
  PY psutil
  PY yt-dlp

  PYU

  UPDATE
  UPGRADE
  SYSUP
""")


# ============================================================
#                    DETECTAR GESTOR
# ============================================================

def detect_package_manager():

    if command_exists("pkg"):

        return "pkg"

    if command_exists("apt"):

        return "apt"

    return None


# ============================================================
#                          INSTALAR
# ============================================================

def install_package(package, manager=None):

    if not package:

        print(
            "✗ Debes indicar un paquete."
        )

        return

    if manager is None:

        manager = detect_package_manager()

    if manager is None:

        print(
            "✗ No se encontró pkg ni apt."
        )

        return

    print()
    print(
        f"📦 Instalando {package} con {manager}..."
    )
    print()

    if manager == "pkg":

        run_command(
            [
                "pkg",
                "install",
                "-y",
                package
            ]
        )

    elif manager == "apt":

        run_command(
            [
                "apt",
                "install",
                "-y",
                package
            ]
        )


# ============================================================
#                        DESINSTALAR
# ============================================================

def uninstall_package(package):

    if not package:

        print(
            "✗ Debes indicar un paquete."
        )

        return

    manager = detect_package_manager()

    if manager is None:

        print(
            "✗ No se encontró pkg ni apt."
        )

        return

    print()
    print(
        f"⚠ Vas a desinstalar: {package}"
    )

    if not confirm(
        "¿Continuar?"
    ):

        print(
            "Operación cancelada."
        )

        return

    print()

    if manager == "pkg":

        run_command(
            [
                "pkg",
                "uninstall",
                "-y",
                package
            ]
        )

    else:

        run_command(
            [
                "apt",
                "remove",
                "-y",
                package
            ]
        )


# ============================================================
#                           BUSCAR
# ============================================================

def search_package(package):

    if not package:

        print(
            "✗ Debes indicar qué buscar."
        )

        return

    manager = detect_package_manager()

    if manager is None:

        print(
            "✗ No se encontró pkg ni apt."
        )

        return

    print()
    print(
        f"🔎 Buscando: {package}"
    )
    print()

    if manager == "pkg":

        run_command(
            [
                "pkg",
                "search",
                package
            ]
        )

    else:

        run_command(
            [
                "apt-cache",
                "search",
                package
            ]
        )


# ============================================================
#                       PYTHON / PIP
# ============================================================

def python_available():

    return (
        command_exists("python")
        or command_exists("python3")
    )


def python_command():

    if command_exists("python"):

        return "python"

    if command_exists("python3"):

        return "python3"

    return None


def pip_install(package):

    python = python_command()

    if python is None:

        print(
            "✗ Python no está instalado."
        )

        print(
            "Instálalo con:"
        )

        print(
            "pkg install python"
        )

        return

    print()
    print(
        f"🐍 Instalando {package} con pip..."
    )
    print()

    run_command(
        [
            python,
            "-m",
            "pip",
            "install",
            package
        ]
    )


def pip_upgrade():

    python = python_command()

    if python is None:

        print(
            "✗ Python no está instalado."
        )

        return

    print()
    print(
        "🐍 Comprobando paquetes Python..."
    )
    print()

    result = run_command(
        [
            python,
            "-m",
            "pip",
            "list",
            "--outdated"
        ]
    )

    if result is None:
        return

    print()

    if result.returncode != 0:

        print(
            "✗ No se pudo consultar pip."
        )

        return

    print(
        "⬆ Actualizando paquetes Python..."
    )
    print()

    run_command(
        [
            python,
            "-m",
            "pip",
            "list",
            "--outdated",
            "--format=freeze"
        ]
    )

    print()

    print(
        "Para actualizar un paquete concreto:"
    )

    print(
        "PY <paquete>"
    )

    print()

    print(
        "Actualizando pip..."
    )

    run_command(
        [
            python,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip"
        ]
    )


# ============================================================
#                         UPDATE
# ============================================================

def update_packages():

    manager = detect_package_manager()

    if manager is None:

        print(
            "✗ No se encontró pkg ni apt."
        )

        return

    print()
    print(
        "🔄 Actualizando índices..."
    )
    print()

    if manager == "pkg":

        run_command(
            [
                "pkg",
                "update"
            ]
        )

    else:

        run_command(
            [
                "apt",
                "update"
            ]
        )


# ============================================================
#                         UPGRADE
# ============================================================

def upgrade_packages():

    manager = detect_package_manager()

    if manager is None:

        print(
            "✗ No se encontró pkg ni apt."
        )

        return

    print()
    print(
        "⬆ Actualizando paquetes del sistema..."
    )
    print()

    if manager == "pkg":

        run_command(
            [
                "pkg",
                "upgrade",
                "-y"
            ]
        )

    else:

        run_command(
            [
                "apt",
                "upgrade",
                "-y"
            ]
        )


# ============================================================
#                         SYSUP
# ============================================================

def system_upgrade():

    print("""
╔══════════════════════════════════════╗
║       Actualización de LynaOS        ║
╚══════════════════════════════════════╝
""")

    print(
        "Paso 1/3: Actualizando índices..."
    )

    update_packages()

    print()
    print(
        "Paso 2/3: Actualizando paquetes..."
    )

    upgrade_packages()

    print()
    print(
        "Paso 3/3: Actualizando Python..."
    )

    pip_upgrade()

    print()
    print(
        "✓ Actualización del sistema finalizada."
    )


# ============================================================
#                           INFO
# ============================================================

def system_info():

    manager = detect_package_manager()

    print("""
╔══════════════════════════════════════╗
║          Información LynaStore       ║
╚══════════════════════════════════════╝
""")

    print(
        f"LynaStore:        {APP_VERSION}"
    )

    if manager:

        print(
            f"Gestor detectado: {manager}"
        )

    else:

        print(
            "Gestor detectado: ninguno"
        )

    print(
        f"pkg disponible:    "
        f"{'Sí' if command_exists('pkg') else 'No'}"
    )

    print(
        f"apt disponible:    "
        f"{'Sí' if command_exists('apt') else 'No'}"
    )

    print(
        f"python disponible: "
        f"{'Sí' if python_available() else 'No'}"
    )

    print(
        f"git disponible:    "
        f"{'Sí' if command_exists('git') else 'No'}"
    )

    print(
        f"pip disponible:    "
        f"{'Sí' if python_available() else 'No'}"
    )


# ============================================================
#                           APP
# ============================================================

def run():

    banner()

    while True:

        try:

            command = input(
                "lynastore> "
            ).strip()

        except KeyboardInterrupt:

            print()
            print(
                "Saliendo de LynaStore..."
            )

            break

        except EOFError:

            print()
            break

        if not command:
            continue

        parts = command.split()

        action = parts[0].upper()

        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        if action in (
            "Q",
            "EXIT"
        ):

            print(
                "Saliendo de LynaStore..."
            )

            break

        # ----------------------------------------------------
        # AYUDA
        # ----------------------------------------------------

        elif action in (
            "H",
            "HELP"
        ):

            help_command()

        # ----------------------------------------------------
        # INSTALAR
        # ----------------------------------------------------

        elif action in (
            "I",
            "INSTALL"
        ):

            if len(parts) < 2:

                print(
                    "Uso: I <paquete>"
                )

                continue

            install_package(
                " ".join(parts[1:])
            )

        # ----------------------------------------------------
        # DESINSTALAR
        # ----------------------------------------------------

        elif action in (
            "U",
            "UNINSTALL"
        ):

            if len(parts) < 2:

                print(
                    "Uso: U <paquete>"
                )

                continue

            uninstall_package(
                " ".join(parts[1:])
            )

        # ----------------------------------------------------
        # BUSCAR
        # ----------------------------------------------------

        elif action in (
            "S",
            "SEARCH"
        ):

            if len(parts) < 2:

                print(
                    "Uso: S <paquete>"
                )

                continue

            search_package(
                " ".join(parts[1:])
            )

        # ----------------------------------------------------
        # PKG
        # ----------------------------------------------------

        elif action == "P":

            if len(parts) < 2:

                print(
                    "Uso: P <paquete>"
                )

                continue

            install_package(
                " ".join(parts[1:]),
                "pkg"
            )

        # ----------------------------------------------------
        # APT
        # ----------------------------------------------------

        elif action == "A":

            if len(parts) < 2:

                print(
                    "Uso: A <paquete>"
                )

                continue

            install_package(
                " ".join(parts[1:]),
                "apt"
            )

        # ----------------------------------------------------
        # PYTHON / PIP
        # ----------------------------------------------------

        elif action in (
            "PY",
            "PIP"
        ):

            if len(parts) < 2:

                print(
                    "Uso: PY <paquete>"
                )

                continue

            pip_install(
                " ".join(parts[1:])
            )

        # ----------------------------------------------------
        # PYU
        # ----------------------------------------------------

        elif action == "PYU":

            pip_upgrade()

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

        elif action == "UPDATE":

            update_packages()

        # ----------------------------------------------------
        # UPGRADE
        # ----------------------------------------------------

        elif action == "UPGRADE":

            upgrade_packages()

        # ----------------------------------------------------
        # SYSUP
        # ----------------------------------------------------

        elif action in (
            "SYSUP",
            "FULLUPGRADE"
        ):

            system_upgrade()

        # ----------------------------------------------------
        # INFO
        # ----------------------------------------------------

        elif action == "INFO":

            system_info()

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        elif action == "CLEAR":

            os.system("clear")

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
