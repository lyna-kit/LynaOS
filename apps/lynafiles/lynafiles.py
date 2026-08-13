#!/usr/bin/env python3

import os
import shutil
from pathlib import Path


APP_NAME = "LynaFiles"
APP_VERSION = "0.1"

LYNAOS_ROOT = Path.home() / ".lynaos" / "root"
HOME_DIR = LYNAOS_ROOT / "home" / "lyna"

current_dir = HOME_DIR


# ============================================================
#                         UTILIDADES
# ============================================================

def inside_root(path):
    try:
        path.resolve().relative_to(
            LYNAOS_ROOT.resolve()
        )
        return True
    except ValueError:
        return False


def resolve_path(path):

    if not path:
        return current_dir.resolve()

    if path == "~":
        return HOME_DIR.resolve()

    if path.startswith("~/"):
        return (
            HOME_DIR / path[2:]
        ).resolve()

    if path.startswith("/"):
        return (
            LYNAOS_ROOT / path.lstrip("/")
        ).resolve()

    return (
        current_dir / path
    ).resolve()


def display_path(path):

    try:

        relative = path.resolve().relative_to(
            LYNAOS_ROOT.resolve()
        )

        if str(relative) == ".":
            return "/"

        return "/" + str(relative)

    except ValueError:
        return "?"


# ============================================================
#                           ABOUT
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Gestor de archivos oficial de LynaOS.

Sistema de archivos: LynaFS
Raíz: {LYNAOS_ROOT}
""")


# ============================================================
#                            LS
# ============================================================

def list_directory(path=None):

    target = (
        resolve_path(path)
        if path
        else current_dir
    )

    if not inside_root(target):

        print("LynaFiles: acceso fuera de LynaOS.")
        return

    if not target.exists():

        print("LynaFiles: ruta inexistente.")
        return

    if not target.is_dir():

        print("LynaFiles: no es un directorio.")
        return

    print(
        f"\n{display_path(target)}\n"
    )

    items = sorted(
        target.iterdir(),
        key=lambda x: (
            not x.is_dir(),
            x.name.lower()
        )
    )

    if not items:

        print("(vacío)")
        return

    for item in items:

        if item.is_dir():

            print(f"📁 {item.name}")

        else:

            print(f"📄 {item.name}")


# ============================================================
#                            CD
# ============================================================

def change_directory(path):

    global current_dir

    target = resolve_path(path)

    if not inside_root(target):

        print("LynaFiles: acceso fuera de LynaOS.")
        return

    if not target.exists():

        print("LynaFiles: directorio inexistente.")
        return

    if not target.is_dir():

        print("LynaFiles: no es un directorio.")
        return

    current_dir = target


# ============================================================
#                           MKDIR
# ============================================================

def make_directory(name):

    target = resolve_path(name)

    if not inside_root(target):

        print("LynaFiles: acceso fuera de LynaOS.")
        return

    try:

        target.mkdir(
            parents=True,
            exist_ok=False
        )

        print(
            f"Directorio creado: {display_path(target)}"
        )

    except FileExistsError:

        print("LynaFiles: ya existe.")

    except Exception as error:

        print(
            f"LynaFiles: {error}"
        )


# ============================================================
#                           TOUCH
# ============================================================

def create_file(name):

    target = resolve_path(name)

    if not inside_root(target):

        print("LynaFiles: acceso fuera de LynaOS.")
        return

    try:

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        target.touch(
            exist_ok=True
        )

        print(
            f"Archivo creado: {display_path(target)}"
        )

    except Exception as error:

        print(
            f"LynaFiles: {error}"
        )


# ============================================================
#                            CAT
# ============================================================

def read_file(name):

    target = resolve_path(name)

    if not inside_root(target):

        print("LynaFiles: acceso fuera de LynaOS.")
        return

    if not target.exists():

        print("LynaFiles: archivo inexistente.")
        return

    if target.is_dir():

        print("LynaFiles: es un directorio.")
        return

    try:

        print(
            target.read_text()
        )

    except UnicodeDecodeError:

        print(
            "LynaFiles: archivo binario."
        )

    except Exception as error:

        print(
            f"LynaFiles: {error}"
        )


# ============================================================
#                             RM
# ============================================================

def remove(name):

    target = resolve_path(name)

    if not inside_root(target):

        print("LynaFiles: acceso fuera de LynaOS.")
        return

    if target == LYNAOS_ROOT:

        print("LynaFiles: no puedes eliminar la raíz.")
        return

    if not target.exists():

        print("LynaFiles: no existe.")
        return

    try:

        if target.is_dir():

            shutil.rmtree(target)

        else:

            target.unlink()

        print(
            f"Eliminado: {display_path(target)}"
        )

    except Exception as error:

        print(
            f"LynaFiles: {error}"
        )


# ============================================================
#                            COPY
# ============================================================

def copy(source, destination):

    source = resolve_path(source)
    destination = resolve_path(destination)

    if not inside_root(source):
        print("LynaFiles: origen fuera de LynaOS.")
        return

    if not inside_root(destination):
        print("LynaFiles: destino fuera de LynaOS.")
        return

    if not source.exists():
        print("LynaFiles: origen inexistente.")
        return

    try:

        if source.is_dir():

            shutil.copytree(
                source,
                destination,
                dirs_exist_ok=True
            )

        else:

            destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.copy2(
                source,
                destination
            )

        print("Copia realizada.")

    except Exception as error:

        print(
            f"LynaFiles: {error}"
        )


# ============================================================
#                             MOVE
# ============================================================

def move(source, destination):

    source = resolve_path(source)
    destination = resolve_path(destination)

    if not inside_root(source):
        print("LynaFiles: origen fuera de LynaOS.")
        return

    if not inside_root(destination):
        print("LynaFiles: destino fuera de LynaOS.")
        return

    if not source.exists():
        print("LynaFiles: origen inexistente.")
        return

    try:

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.move(
            str(source),
            str(destination)
        )

        print("Movimiento realizado.")

    except Exception as error:

        print(
            f"LynaFiles: {error}"
        )


# ============================================================
#                            TREE
# ============================================================

def tree(path=None):

    target = (
        resolve_path(path)
        if path
        else current_dir
    )

    if not inside_root(target):

        print("LynaFiles: acceso fuera de LynaOS.")
        return

    if not target.exists():

        print("LynaFiles: ruta inexistente.")
        return

    print(
        f"📁 {target.name or '/'}"
    )

    def walk(directory, prefix=""):

        items = sorted(
            directory.iterdir(),
            key=lambda x: (
                not x.is_dir(),
                x.name.lower()
            )
        )

        for index, item in enumerate(items):

            last = index == len(items) - 1

            branch = (
                "└── "
                if last
                else "├── "
            )

            icon = (
                "📁 "
                if item.is_dir()
                else "📄 "
            )

            print(
                prefix
                + branch
                + icon
                + item.name
            )

            if item.is_dir():

                walk(
                    item,
                    prefix
                    + (
                        "    "
                        if last
                        else "│   "
                    )
                )

    if target.is_dir():

        walk(target)


# ============================================================
#                            HELP
# ============================================================

def help_command():

    print("""
LynaFiles 0.1

Comandos:

  ls [ruta]             Listar archivos
  cd <ruta>             Cambiar directorio
  pwd                   Mostrar ubicación
  mkdir <nombre>        Crear carpeta
  touch <archivo>       Crear archivo
  cat <archivo>         Leer archivo
  rm <ruta>             Eliminar
  cp <origen> <destino> Copiar
  mv <origen> <destino> Mover
  tree [ruta]           Mostrar árbol
  about                 Información
  help                  Ayuda
  clear                 Limpiar pantalla
  exit                  Salir
""")


# ============================================================
#                          TERMINAL
# ============================================================

def run():

    global current_dir

    print(f"""
╔══════════════════════════════════╗
║         {APP_NAME} {APP_VERSION}         ║
║        Gestor de archivos       ║
╚══════════════════════════════════╝
""")

    while True:

        try:

            command = input(
                f"lynafiles:{display_path(current_dir)}$ "
            ).strip()

            if not command:
                continue

            parts = command.split()

            cmd = parts[0]
            args = parts[1:]

            if cmd == "exit":
                break

            elif cmd == "help":
                help_command()

            elif cmd == "about":
                about()

            elif cmd == "clear":
                os.system("clear")

            elif cmd == "ls":
                list_directory(
                    args[0]
                    if args
                    else None
                )

            elif cmd == "cd":

                if not args:
                    change_directory("~")
                else:
                    change_directory(args[0])

            elif cmd == "pwd":

                print(
                    display_path(current_dir)
                )

            elif cmd == "mkdir":

                if not args:
                    print("Uso: mkdir <nombre>")
                else:
                    make_directory(args[0])

            elif cmd == "touch":

                if not args:
                    print("Uso: touch <archivo>")
                else:
                    create_file(args[0])

            elif cmd == "cat":

                if not args:
                    print("Uso: cat <archivo>")
                else:
                    read_file(args[0])

            elif cmd == "rm":

                if not args:
                    print("Uso: rm <ruta>")
                else:
                    remove(args[0])

            elif cmd == "cp":

                if len(args) < 2:
                    print(
                        "Uso: cp <origen> <destino>"
                    )
                else:
                    copy(
                        args[0],
                        args[1]
                    )

            elif cmd == "mv":

                if len(args) < 2:
                    print(
                        "Uso: mv <origen> <destino>"
                    )
                else:
                    move(
                        args[0],
                        args[1]
                    )

            elif cmd == "tree":

                tree(
                    args[0]
                    if args
                    else None
                )

            else:

                print(
                    f"LynaFiles: comando desconocido: {cmd}"
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
