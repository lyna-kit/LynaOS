#!/usr/bin/env python3

import os
import shutil
import subprocess


APP_NAME = "LynaStore"
APP_VERSION = "0.3"


# ============================================================
#                         UTILIDADES
# ============================================================

def command_exists(command):

    return shutil.which(command) is not None


def run_command(command):

    try:

        subprocess.run(
            command,
            check=False
        )

    except KeyboardInterrupt:

        print()
        print("Operación cancelada.")

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════╗
║           LynaStore 0.3              ║
║       Gestor de paquetes             ║
╚══════════════════════════════════════╝

Compatible con:

  • pkg
  • apt
""")


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print("""
LynaStore 0.3

Comandos:

  I <paquete>       Instalar paquete
  U <paquete>       Desinstalar paquete
  S <paquete>       Buscar paquete
  P <paquete>       Instalar mediante pkg
  A <paquete>       Instalar mediante apt

  UPDATE            Actualizar índices
  UPGRADE           Actualizar paquetes

  INFO              Información del sistema
  H                 Ayuda
  CLEAR             Limpiar pantalla
  Q                 Salir

Ejemplos:

  S python
  I python
  P git
  A curl
  UPDATE
  UPGRADE
""")


# ============================================================
#                         DETECTAR GESTOR
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
#                         ACTUALIZAR
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
#                          UPGRADE
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
        "⬆ Actualizando paquetes..."
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
        f"LynaStore:       {APP_VERSION}"
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
        f"pkg disponible:   {'Sí' if command_exists('pkg') else 'No'}"
    )

    print(
        f"apt disponible:   {'Sí' if command_exists('apt') else 'No'}"
    )

    print(
        f"python disponible: {'Sí' if command_exists('python') else 'No'}"
    )

    print(
        f"git disponible:    {'Sí' if command_exists('git') else 'No'}"
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
        # SEARCH
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
