#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path


APP_NAME = "LynaStore"
APP_VERSION = "0.1"


# ============================================================
#                         UTILIDADES
# ============================================================

def command_exists(command):
    return shutil.which(command) is not None


def run_command(command):
    try:

        result = subprocess.run(
            command,
            text=True
        )

        return result.returncode

    except FileNotFoundError:

        print(
            f"LynaStore: comando no encontrado: {command[0]}"
        )

        return 127

    except KeyboardInterrupt:

        print(
            "\nOperación cancelada."
        )

        return 130


# ============================================================
#                           BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════╗
║           LynaStore 0.1              ║
║       Tienda de aplicaciones         ║
║             LynaOS                   ║
╚══════════════════════════════════════╝

I = Instalar
U = Desinstalar
S = Buscar
H = Ayuda
P = Instalar por pkg
A = Instalar por apt

Escribe H para obtener ayuda.
""")


# ============================================================
#                            AYUDA
# ============================================================

def help_command():

    print("""
LynaStore 0.1

Comandos:

  I    Instalar una aplicación
  U    Desinstalar una aplicación
  S    Buscar un paquete
  H    Mostrar ayuda
  P    Instalar mediante pkg
  A    Instalar mediante apt
  Q    Salir

Ejemplos:

  I > python
  U > python
  S > python
  P > python
  A > curl
""")


# ============================================================
#                           BUSCAR
# ============================================================

def search_package(package):

    package = package.strip()

    if not package:

        print(
            "LynaStore: debes indicar un paquete."
        )

        return

    print(
        f"\nBuscando '{package}'...\n"
    )

    if command_exists("pkg"):

        run_command(
            [
                "pkg",
                "search",
                package
            ]
        )

    else:

        print(
            "LynaStore: pkg no está disponible."
        )


# ============================================================
#                       INSTALAR CON PKG
# ============================================================

def install_pkg(package):

    package = package.strip()

    if not package:

        print(
            "LynaStore: debes indicar un paquete."
        )

        return

    if not command_exists("pkg"):

        print(
            "LynaStore: pkg no está disponible."
        )

        return

    print(
        f"\nInstalando '{package}' mediante pkg...\n"
    )

    run_command(
        [
            "pkg",
            "install",
            "-y",
            package
        ]
    )


# ============================================================
#                       INSTALAR CON APT
# ============================================================

def install_apt(package):

    package = package.strip()

    if not package:

        print(
            "LynaStore: debes indicar un paquete."
        )

        return

    if not command_exists("apt"):

        print(
            "LynaStore: apt no está disponible."
        )

        return

    print(
        f"\nInstalando '{package}' mediante apt...\n"
    )

    run_command(
        [
            "apt",
            "install",
            "-y",
            package
        ]
    )


# ============================================================
#                         INSTALAR
# ============================================================

def install(package):

    package = package.strip()

    if not package:

        print(
            "LynaStore: debes indicar una aplicación."
        )

        return

    print(f"""
¿Cómo quieres instalar '{package}'?

P = pkg
A = apt
L = LynaPkg
Q = Cancelar
""")

    method = input(
        "Método> "
    ).strip().upper()

    if method == "P":

        install_pkg(package)

    elif method == "A":

        install_apt(package)

    elif method == "L":

        print(
            "\nLynaPkg todavía está siendo integrado con LynaStore."
        )

    elif method == "Q":

        print(
            "Instalación cancelada."
        )

    else:

        print(
            "Método no válido."
        )


# ============================================================
#                        DESINSTALAR
# ============================================================

def uninstall(package):

    package = package.strip()

    if not package:

        print(
            "LynaStore: debes indicar un paquete."
        )

        return

    print(f"""
¿Cómo quieres desinstalar '{package}'?

P = pkg
A = apt
Q = Cancelar
""")

    method = input(
        "Método> "
    ).strip().upper()

    if method == "P":

        if not command_exists("pkg"):

            print(
                "LynaStore: pkg no está disponible."
            )

            return

        run_command(
            [
                "pkg",
                "uninstall",
                "-y",
                package
            ]
        )

    elif method == "A":

        if not command_exists("apt"):

            print(
                "LynaStore: apt no está disponible."
            )

            return

        run_command(
            [
                "apt",
                "remove",
                "-y",
                package
            ]
        )

    elif method == "Q":

        print(
            "Desinstalación cancelada."
        )

    else:

        print(
            "Método no válido."
        )


# ============================================================
#                         INFORMACIÓN
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Tienda de aplicaciones de LynaOS.

Funciones:
  • Buscar paquetes
  • Instalar mediante pkg
  • Instalar mediante apt
  • Desinstalar paquetes

LynaStore forma parte del ecosistema LynaOS.
""")


# ============================================================
#                         APLICACIÓN
# ============================================================

def run():

    banner()

    while True:

        try:

            command = input(
                "LynaStore> "
            ).strip()

            if not command:
                continue

            # ------------------------------------------------
            # SALIR
            # ------------------------------------------------

            if command.upper() in (
                "Q",
                "EXIT"
            ):

                print(
                    "Saliendo de LynaStore..."
                )

                break

            # ------------------------------------------------
            # AYUDA
            # ------------------------------------------------

            elif command.upper() == "H":

                help_command()

            # ------------------------------------------------
            # ABOUT
            # ------------------------------------------------

            elif command.lower() == "about":

                about()

            # ------------------------------------------------
            # INSTALAR
            # ------------------------------------------------

            elif command.upper().startswith("I"):

                if ">" in command:

                    package = command.split(
                        ">",
                        1
                    )[1].strip()

                else:

                    package = input(
                        "Aplicación> "
                    ).strip()

                install(package)

            # ------------------------------------------------
            # DESINSTALAR
            # ------------------------------------------------

            elif command.upper().startswith("U"):

                if ">" in command:

                    package = command.split(
                        ">",
                        1
                    )[1].strip()

                else:

                    package = input(
                        "Aplicación> "
                    ).strip()

                uninstall(package)

            # ------------------------------------------------
            # BUSCAR
            # ------------------------------------------------

            elif command.upper().startswith("S"):

                if ">" in command:

                    package = command.split(
                        ">",
                        1
                    )[1].strip()

                else:

                    package = input(
                        "Buscar> "
                    ).strip()

                search_package(package)

            # ------------------------------------------------
            # PKG
            # ------------------------------------------------

            elif command.upper().startswith("P"):

                if ">" in command:

                    package = command.split(
                        ">",
                        1
                    )[1].strip()

                else:

                    package = input(
                        "Paquete pkg> "
                    ).strip()

                install_pkg(package)

            # ------------------------------------------------
            # APT
            # ------------------------------------------------

            elif command.upper().startswith("A"):

                if ">" in command:

                    package = command.split(
                        ">",
                        1
                    )[1].strip()

                else:

                    package = input(
                        "Paquete apt> "
                    ).strip()

                install_apt(package)

            # ------------------------------------------------
            # CLEAR
            # ------------------------------------------------

            elif command.lower() == "clear":

                os.system("clear")

            else:

                print(
                    "LynaStore: comando desconocido."
                )

                print(
                    "Escribe H para obtener ayuda."
                )

        except KeyboardInterrupt:

            print(
                "\nOperación cancelada."
            )

        except EOFError:

            break


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":
    run()
