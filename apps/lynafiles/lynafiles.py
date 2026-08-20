#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from pathlib import Path


APP_NAME = "LynaFiles"
APP_VERSION = "0.4"


# ============================================================
#                         ESTADO
# ============================================================

current_dir = Path.cwd()
history = []


# ============================================================
#                       UTILIDADES
# ============================================================

def clear():
    os.system("clear")


def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size)

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


def format_permissions(path):

    try:
        mode = path.stat().st_mode

        permissions = ""

        permissions += "d" if path.is_dir() else "-"

        permissions += "r" if mode & 0o400 else "-"
        permissions += "w" if mode & 0o200 else "-"
        permissions += "x" if mode & 0o100 else "-"

        permissions += "r" if mode & 0o040 else "-"
        permissions += "w" if mode & 0o020 else "-"
        permissions += "x" if mode & 0o010 else "-"

        permissions += "r" if mode & 0o004 else "-"
        permissions += "w" if mode & 0o002 else "-"
        permissions += "x" if mode & 0o001 else "-"

        return permissions

    except Exception:
        return "----------"


def resolve_path(value):

    path = Path(value).expanduser()

    if not path.is_absolute():
        path = current_dir / path

    try:
        return path.resolve()
    except Exception:
        return path.absolute()


def display_name(path):

    if path.name:
        return path.name

    return str(path)


def is_safe_path(path):

    try:
        path.resolve()
        return True
    except Exception:
        return False


def pause():

    input("\nPresiona ENTER para continuar...")


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print(f"""
╔══════════════════════════════════════════════════════════╗
║                    {APP_NAME} {APP_VERSION}                       ║
║                 Administrador de archivos               ║
╚══════════════════════════════════════════════════════════╝
""")


# ============================================================
#                           LIST
# ============================================================

def list_files():

    try:
        entries = list(current_dir.iterdir())

    except PermissionError:
        print("✗ Permiso denegado.")
        return

    except Exception as error:
        print(f"✗ Error: {error}")
        return

    entries.sort(
        key=lambda item: (
            not item.is_dir(),
            item.name.lower()
        )
    )

    print()
    print(f"Ruta: {current_dir}")
    print("─" * 70)

    if not entries:
        print("(directorio vacío)")
        return

    print(
        f"{'#':>3}  "
        f"{'TIPO':<5} "
        f"{'TAMAÑO':>12}  "
        f"NOMBRE"
    )

    print("─" * 70)

    for index, entry in enumerate(entries, start=1):

        try:
            if entry.is_dir():
                kind = "DIR"
                size = "-"
            elif entry.is_symlink():
                kind = "LINK"
                size = "-"
            else:
                kind = "FILE"
                size = format_size(
                    entry.stat().st_size
                )

        except Exception:
            kind = "?"
            size = "?"

        print(
            f"{index:>3}  "
            f"{kind:<5} "
            f"{size:>12}  "
            f"{entry.name}"
        )

    print("─" * 70)


def get_entries():

    try:
        entries = list(current_dir.iterdir())

        entries.sort(
            key=lambda item: (
                not item.is_dir(),
                item.name.lower()
            )
        )

        return entries

    except Exception:
        return []


def get_entry(number):

    entries = get_entries()

    try:
        index = int(number) - 1
    except ValueError:
        print("✗ Número inválido.")
        return None

    if index < 0 or index >= len(entries):
        print("✗ No existe ese elemento.")
        return None

    return entries[index]


# ============================================================
#                           CD
# ============================================================

def change_directory(target):

    global current_dir
    global history

    if not target:
        target = str(Path.home())

    path = resolve_path(target)

    if not path.exists():
        print("✗ El directorio no existe.")
        return

    if not path.is_dir():
        print("✗ No es un directorio.")
        return

    try:
        path = path.resolve()

        history.append(current_dir)

        current_dir = path

    except Exception as error:
        print(f"✗ No se pudo cambiar de directorio: {error}")


def back_directory():

    global current_dir

    if history:

        current_dir = history.pop()
        return

    parent = current_dir.parent

    if parent == current_dir:
        print("Ya estás en la raíz.")
        return

    current_dir = parent


# ============================================================
#                           OPEN
# ============================================================

def open_file(target):

    path = get_target_path(target)

    if path is None:
        return

    if not path.exists():
        print("✗ El archivo no existe.")
        return

    if path.is_dir():

        change_directory(str(path))
        return

    print(
        f"▶ Abriendo: {path.name}"
    )

    try:

        if sys.platform.startswith("linux"):

            if shutil.which("termux-open"):
                subprocess.run(
                    ["termux-open", str(path)],
                    check=False
                )

            elif shutil.which("xdg-open"):
                subprocess.run(
                    ["xdg-open", str(path)],
                    check=False
                )

            else:
                print(
                    "No se encontró termux-open ni xdg-open."
                )

        elif sys.platform == "darwin":

            subprocess.run(
                ["open", str(path)],
                check=False
            )

        elif os.name == "nt":

            os.startfile(str(path))

        else:
            print(
                "Sistema operativo no compatible."
            )

    except Exception as error:
        print(f"✗ Error al abrir: {error}")


# ============================================================
#                         OBTENER RUTA
# ============================================================

def get_target_path(value):

    if not value:
        print("✗ Debes indicar un archivo.")
        return None

    try:
        number = int(value)

        entry = get_entry(str(number))

        return entry

    except ValueError:
        return resolve_path(value)


# ============================================================
#                           COPY
# ============================================================

def copy_item(source, destination):

    source_path = get_target_path(source)

    if source_path is None:
        return

    destination_path = resolve_path(destination)

    if not source_path.exists():
        print("✗ El origen no existe.")
        return

    try:

        if source_path.is_dir():

            if destination_path.exists():

                final_destination = (
                    destination_path
                    / source_path.name
                )

            else:

                final_destination = destination_path

            shutil.copytree(
                source_path,
                final_destination,
                dirs_exist_ok=True
            )

        else:

            if destination_path.is_dir():

                destination_path = (
                    destination_path
                    / source_path.name
                )

            shutil.copy2(
                source_path,
                destination_path
            )

        print(
            f"✓ Copiado: {source_path.name}"
        )

    except Exception as error:

        print(
            f"✗ No se pudo copiar: {error}"
        )


# ============================================================
#                           MOVE
# ============================================================

def move_item(source, destination):

    source_path = get_target_path(source)

    if source_path is None:
        return

    destination_path = resolve_path(destination)

    if not source_path.exists():
        print("✗ El origen no existe.")
        return

    try:

        if destination_path.is_dir():

            destination_path = (
                destination_path
                / source_path.name
            )

        shutil.move(
            str(source_path),
            str(destination_path)
        )

        print(
            f"✓ Movido: {source_path.name}"
        )

    except Exception as error:

        print(
            f"✗ No se pudo mover: {error}"
        )


# ============================================================
#                         REMOVE
# ============================================================

def remove_item(target):

    path = get_target_path(target)

    if path is None:
        return

    if not path.exists() and not path.is_symlink():
        print("✗ El elemento no existe.")
        return

    print()
    print(
        f"⚠ Vas a eliminar: {path}"
    )

    if path.is_dir():
        print(
            "⚠ Esto eliminará el directorio y su contenido."
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
        print("Operación cancelada.")
        return

    try:

        if path.is_dir() and not path.is_symlink():

            shutil.rmtree(path)

        else:

            path.unlink()

        print(
            "✓ Elemento eliminado."
        )

    except PermissionError:
        print(
            "✗ Permiso denegado."
        )

    except Exception as error:
        print(
            f"✗ Error eliminando: {error}"
        )


# ============================================================
#                         MKDIR
# ============================================================

def make_directory(name):

    if not name:
        print("✗ Debes indicar un nombre.")
        return

    path = resolve_path(name)

    try:

        path.mkdir(
            parents=True,
            exist_ok=False
        )

        print(
            f"✓ Directorio creado: {path.name}"
        )

    except FileExistsError:

        print(
            "✗ Ese directorio ya existe."
        )

    except Exception as error:

        print(
            f"✗ No se pudo crear: {error}"
        )


# ============================================================
#                           TOUCH
# ============================================================

def touch_file(name):

    if not name:
        print("✗ Debes indicar un nombre.")
        return

    path = resolve_path(name)

    try:

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.touch(
            exist_ok=False
        )

        print(
            f"✓ Archivo creado: {path.name}"
        )

    except FileExistsError:

        print(
            "✗ Ese archivo ya existe."
        )

    except Exception as error:

        print(
            f"✗ No se pudo crear: {error}"
        )


# ============================================================
#                         RENAME
# ============================================================

def rename_item(source, new_name):

    path = get_target_path(source)

    if path is None:
        return

    if not path.exists():
        print("✗ El elemento no existe.")
        return

    if not new_name:
        print("✗ Debes indicar un nuevo nombre.")
        return

    destination = path.parent / new_name

    if destination.exists():
        print("✗ Ya existe un elemento con ese nombre.")
        return

    try:

        path.rename(destination)

        print(
            f"✓ Renombrado a: {new_name}"
        )

    except Exception as error:

        print(
            f"✗ No se pudo renombrar: {error}"
        )


# ============================================================
#                          SEARCH
# ============================================================

def search_files(text):

    if not text:
        print("✗ Debes indicar qué buscar.")
        return

    print()
    print(
        f"🔎 Buscando '{text}' en:"
    )
    print(
        current_dir
    )
    print()

    found = 0

    try:

        for path in current_dir.rglob("*"):

            if text.lower() in path.name.lower():

                print(path)

                found += 1

                if found >= 500:
                    print(
                        "\nSe alcanzó el límite de 500 resultados."
                    )
                    break

    except PermissionError:
        print(
            "⚠ Se encontraron directorios sin permisos."
        )

    except Exception as error:
        print(
            f"✗ Error durante la búsqueda: {error}"
        )

    if found == 0:
        print(
            "No se encontraron resultados."
        )


# ============================================================
#                           INFO
# ============================================================

def item_info(target):

    path = get_target_path(target)

    if path is None:
        return

    if not path.exists() and not path.is_symlink():
        print("✗ El elemento no existe.")
        return

    try:

        stat = path.stat()

        print(f"""
╔══════════════════════════════════════════════════════════╗
║                  Información                            ║
╚══════════════════════════════════════════════════════════╝

Nombre:       {path.name}
Ruta:         {path}
Tipo:         {"Directorio" if path.is_dir() else "Archivo"}
Tamaño:       {format_size(stat.st_size)}
Permisos:     {format_permissions(path)}
""")


        if path.is_file():

            print(
                f"Extensión:    {path.suffix or '(ninguna)'}"
            )

    except PermissionError:
        print("✗ Permiso denegado.")

    except Exception as error:
        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                           HELP
# ============================================================

def help_command():

    print("""
LynaFiles 0.4

Navegación:

  LS                 Listar archivos
  CD <ruta>          Entrar en directorio
  BACK               Volver al directorio anterior

Archivos:

  OPEN <n>           Abrir archivo
  INFO <n>           Información
  SEARCH <texto>     Buscar

Operaciones:

  CP <origen> <dest> Copiar
  MV <origen> <dest> Mover
  RM <n>              Eliminar
  RENAME <n> <nombre> Renombrar

Crear:

  MKDIR <nombre>     Crear directorio
  TOUCH <nombre>     Crear archivo

Sistema:

  CLEAR              Limpiar pantalla
  PWD                Mostrar ruta actual
  HELP               Ayuda
  Q                  Salir


Puedes usar números para seleccionar
elementos de la lista.

Ejemplos:

  LS
  CD apps
  CD 1
  OPEN 2
  INFO 3
  CP 1 ../backup
  MV 2 ../
  RM 4
  MKDIR pruebas
  TOUCH ejemplo.txt
  RENAME 1 nuevo.txt
  SEARCH python
  BACK
""")


# ============================================================
#                           PWD
# ============================================================

def print_working_directory():

    print(
        current_dir
    )


# ============================================================
#                         PROCESADOR
# ============================================================

def process_command(command):

    global current_dir

    parts = command.split()

    if not parts:
        return True

    action = parts[0].upper()

    # --------------------------------------------------------
    # SALIR
    # --------------------------------------------------------

    if action in ("Q", "QUIT", "EXIT"):

        return False

    # --------------------------------------------------------
    # LIST
    # --------------------------------------------------------

    elif action in ("LS", "LIST", "DIR"):

        list_files()

    # --------------------------------------------------------
    # CD
    # --------------------------------------------------------

    elif action == "CD":

        if len(parts) < 2:
            change_directory(str(Path.home()))
        else:
            change_directory(
                " ".join(parts[1:])
            )

    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    elif action in ("BACK", ".."):

        back_directory()

    # --------------------------------------------------------
    # OPEN
    # --------------------------------------------------------

    elif action in ("OPEN", "O"):

        if len(parts) < 2:
            print("Uso: OPEN <número|ruta>")
        else:
            open_file(parts[1])

    # --------------------------------------------------------
    # COPY
    # --------------------------------------------------------

    elif action in ("CP", "COPY"):

        if len(parts) < 3:
            print("Uso: CP <origen> <destino>")
        else:
            copy_item(
                parts[1],
                " ".join(parts[2:])
            )

    # --------------------------------------------------------
    # MOVE
    # --------------------------------------------------------

    elif action in ("MV", "MOVE"):

        if len(parts) < 3:
            print("Uso: MV <origen> <destino>")
        else:
            move_item(
                parts[1],
                " ".join(parts[2:])
            )

    # --------------------------------------------------------
    # REMOVE
    # --------------------------------------------------------

    elif action in ("RM", "REMOVE", "DELETE"):

        if len(parts) < 2:
            print("Uso: RM <número|ruta>")
        else:
            remove_item(parts[1])

    # --------------------------------------------------------
    # MKDIR
    # --------------------------------------------------------

    elif action in ("MKDIR", "MD"):

        if len(parts) < 2:
            print("Uso: MKDIR <nombre>")
        else:
            make_directory(
                " ".join(parts[1:])
            )

    # --------------------------------------------------------
    # TOUCH
    # --------------------------------------------------------

    elif action == "TOUCH":

        if len(parts) < 2:
            print("Uso: TOUCH <nombre>")
        else:
            touch_file(
                " ".join(parts[1:])
            )

    # --------------------------------------------------------
    # RENAME
    # --------------------------------------------------------

    elif action in ("RENAME", "REN"):

        if len(parts) < 3:
            print(
                "Uso: RENAME <número|ruta> <nuevo nombre>"
            )
        else:
            rename_item(
                parts[1],
                " ".join(parts[2:])
            )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    elif action in ("SEARCH", "FIND"):

        if len(parts) < 2:
            print("Uso: SEARCH <texto>")
        else:
            search_files(
                " ".join(parts[1:])
            )

    # --------------------------------------------------------
    # INFO
    # --------------------------------------------------------

    elif action == "INFO":

        if len(parts) < 2:
            print("Uso: INFO <número|ruta>")
        else:
            item_info(parts[1])

    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    elif action in ("CLEAR", "CLS"):

        clear()

    # --------------------------------------------------------
    # PWD
    # --------------------------------------------------------

    elif action == "PWD":

        print_working_directory()

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    elif action in ("H", "HELP", "?"):

        help_command()

    # --------------------------------------------------------
    # COMANDO DESCONOCIDO
    # --------------------------------------------------------

    else:

        print(
            "Comando desconocido."
        )

        print(
            "Escribe HELP para ver los comandos."
        )

    return True


# ============================================================
#                            MAIN
# ============================================================

def main():

    global current_dir

    current_dir = Path.cwd().resolve()

    clear()

    banner()

    print(
        f"Ruta inicial: {current_dir}"
    )

    print(
        "Escribe HELP para ver los comandos."
    )

    print()

    while True:

        try:

            command = input(
                "lynafiles> "
            ).strip()

            if not process_command(command):
                break

        except KeyboardInterrupt:

            print()
            print(
                "Operación cancelada."
            )

        except EOFError:

            print()
            break

        except Exception as error:

            print(
                f"✗ Error: {error}"
            )

    print(
        "\nSaliendo de LynaFiles..."
    )


if __name__ == "__main__":
    main()
