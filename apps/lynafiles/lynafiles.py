#!/usr/bin/env python3

import os
import shutil
from pathlib import Path


APP_NAME = "LynaFiles"
APP_VERSION = "0.3"


# ============================================================
#                         UTILIDADES
# ============================================================

def get_path(value):

    path = Path(value).expanduser()

    if not path.is_absolute():
        path = Path.cwd() / path

    return path.resolve()


def format_size(size):

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    value = float(size)

    for unit in units:

        if value < 1024:

            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


def file_type(path):

    if path.is_dir():
        return "Directorio"

    if path.is_file():
        return "Archivo"

    if path.is_symlink():
        return "Enlace"

    return "Desconocido"


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════╗
║          LynaFiles 0.3               ║
║       Gestor de archivos             ║
╚══════════════════════════════════════╝
""")


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print("""
LynaFiles 0.3

Navegación:

  L <ruta>                 Listar contenido
  CD <ruta>                Cambiar directorio
  PWD                      Mostrar directorio actual

Archivos:

  C <archivo>              Crear archivo
  CAT <archivo>            Leer archivo
  INFO <ruta>              Información

Directorios:

  MK <carpeta>             Crear carpeta

Operaciones:

  CP <origen> <destino>    Copiar
  MV <origen> <destino>    Mover / renombrar
  RM <ruta>                Eliminar

Búsqueda:

  SEARCH <texto>           Buscar en el directorio actual

Sistema:

  CLEAR                    Limpiar pantalla
  H                        Ayuda
  Q                        Salir

Ejemplos:

  L .
  CD ~/Download
  C prueba.txt
  MK documentos
  CP prueba.txt documentos/
  MV prueba.txt nuevo.txt
  CAT nuevo.txt
  INFO nuevo.txt
  SEARCH .txt
  RM nuevo.txt
""")


# ============================================================
#                           LISTAR
# ============================================================

def list_directory(path):

    path = get_path(path)

    if not path.exists():

        print(
            "✗ La ruta no existe."
        )

        return

    if not path.is_dir():

        print(
            "✗ La ruta no es un directorio."
        )

        return

    try:

        items = sorted(
            path.iterdir(),
            key=lambda item: (
                not item.is_dir(),
                item.name.lower()
            )
        )

        print()
        print(
            f"📁 {path}"
        )
        print()

        if not items:

            print(
                "(Directorio vacío)"
            )

            return

        for item in items:

            if item.is_dir():

                print(
                    f"📁 {item.name}/"
                )

            elif item.is_file():

                print(
                    f"📄 {item.name}"
                )

            elif item.is_symlink():

                print(
                    f"🔗 {item.name}"
                )

            else:

                print(
                    f"❓ {item.name}"
                )

    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                      CAMBIAR DIRECTORIO
# ============================================================

def change_directory(path):

    target = get_path(path)

    if not target.exists():

        print(
            "✗ El directorio no existe."
        )

        return

    if not target.is_dir():

        print(
            "✗ No es un directorio."
        )

        return

    try:

        os.chdir(target)

        print(
            f"✓ Directorio actual: {Path.cwd()}"
        )

    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                      CREAR ARCHIVO
# ============================================================

def create_file(path):

    target = get_path(path)

    if target.exists():

        print(
            "✗ El archivo o directorio ya existe."
        )

        return

    try:

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        target.touch()

        print(
            f"✓ Archivo creado: {target}"
        )

    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                     CREAR DIRECTORIO
# ============================================================

def create_directory(path):

    target = get_path(path)

    try:

        target.mkdir(
            parents=True,
            exist_ok=False
        )

        print(
            f"✓ Directorio creado: {target}"
        )

    except FileExistsError:

        print(
            "✗ El directorio ya existe."
        )

    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                           COPIAR
# ============================================================

def copy_item(source, destination):

    source = get_path(source)
    destination = get_path(destination)

    if not source.exists():

        print(
            "✗ El origen no existe."
        )

        return

    try:

        if source.is_dir():

            final_destination = destination

            if destination.exists() and destination.is_dir():

                final_destination = (
                    destination / source.name
                )

            shutil.copytree(
                source,
                final_destination
            )

        else:

            if destination.exists() and destination.is_dir():

                destination = (
                    destination / source.name
                )

            shutil.copy2(
                source,
                destination
            )

        print(
            f"✓ Copiado: {source} → {destination}"
        )

    except FileExistsError:

        print(
            "✗ El destino ya existe."
        )

    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                       MOVER / RENOMBRAR
# ============================================================

def move_item(source, destination):

    source = get_path(source)
    destination = get_path(destination)

    if not source.exists():

        print(
            "✗ El origen no existe."
        )

        return

    try:

        if destination.exists() and destination.is_dir():

            destination = (
                destination / source.name
            )

        shutil.move(
            str(source),
            str(destination)
        )

        print(
            f"✓ Movido: {source} → {destination}"
        )

    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                          ELIMINAR
# ============================================================

def remove_item(path):

    target = get_path(path)

    if not target.exists():

        print(
            "✗ La ruta no existe."
        )

        return

    print()
    print(
        f"⚠ Vas a eliminar: {target}"
    )

    if target.is_dir():

        print(
            "Esto eliminará el directorio y "
            "todo su contenido."
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

    try:

        if target.is_dir():

            shutil.rmtree(target)

        else:

            target.unlink()

        print(
            "✓ Eliminado correctamente."
        )

    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                           INFO
# ============================================================

def show_info(path):

    target = get_path(path)

    if not target.exists():

        print(
            "✗ La ruta no existe."
        )

        return

    try:

        stat = target.stat()

        print(f"""
╔══════════════════════════════════════╗
║          Información                 ║
╚══════════════════════════════════════╝

Nombre:       {target.name}
Ruta:         {target}
Tipo:         {file_type(target)}
Tamaño:       {format_size(stat.st_size)}
Permisos:     {oct(stat.st_mode)[-3:]}
""")


    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                       LEER ARCHIVO
# ============================================================

def cat_file(path):

    target = get_path(path)

    if not target.exists():

        print(
            "✗ El archivo no existe."
        )

        return

    if not target.is_file():

        print(
            "✗ No es un archivo."
        )

        return

    try:

        with target.open(
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:

            print()
            print(
                file.read()
            )

    except PermissionError:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                          BUSCAR
# ============================================================

def search_files(text):

    if not text:

        print(
            "✗ Debes indicar qué buscar."
        )

        return

    root = Path.cwd()

    print()
    print(
        f"🔎 Buscando '{text}' en {root}"
    )
    print()

    found = 0

    try:

        for path in root.rglob("*"):

            if text.lower() in path.name.lower():

                print(
                    path.relative_to(root)
                )

                found += 1

    except PermissionError:

        pass

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )

    if found == 0:

        print(
            "No se encontraron resultados."
        )

    else:

        print()
        print(
            f"✓ {found} resultado(s)."
        )


# ============================================================
#                           APP
# ============================================================

def run():

    banner()

    while True:

        try:

            command = input(
                f"\nlynafiles [{Path.cwd()}]> "
            ).strip()

        except KeyboardInterrupt:

            print()

            print(
                "Saliendo de LynaFiles..."
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
                "Saliendo de LynaFiles..."
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
        # CLEAR
        # ----------------------------------------------------

        elif action in (
            "CLEAR",
            "CLS"
        ):

            os.system("clear")

        # ----------------------------------------------------
        # LISTAR
        # ----------------------------------------------------

        elif action in (
            "L",
            "LS"
        ):

            path = (
                " ".join(parts[1:])
                if len(parts) > 1
                else "."
            )

            list_directory(path)

        # ----------------------------------------------------
        # CD
        # ----------------------------------------------------

        elif action == "CD":

            if len(parts) < 2:

                print(
                    "Uso: CD <ruta>"
                )

                continue

            path = " ".join(parts[1:])

            change_directory(path)

        # ----------------------------------------------------
        # PWD
        # ----------------------------------------------------

        elif action == "PWD":

            print(
                Path.cwd()
            )

        # ----------------------------------------------------
        # CREAR ARCHIVO
        # ----------------------------------------------------

        elif action == "C":

            if len(parts) < 2:

                print(
                    "Uso: C <archivo>"
                )

                continue

            path = " ".join(parts[1:])

            create_file(path)

        # ----------------------------------------------------
        # CREAR DIRECTORIO
        # ----------------------------------------------------

        elif action == "MK":

            if len(parts) < 2:

                print(
                    "Uso: MK <carpeta>"
                )

                continue

            path = " ".join(parts[1:])

            create_directory(path)

        # ----------------------------------------------------
        # COPIAR
        # ----------------------------------------------------

        elif action == "CP":

            if len(parts) < 3:

                print(
                    "Uso: CP <origen> <destino>"
                )

                continue

            source = parts[1]
            destination = " ".join(parts[2:])

            copy_item(
                source,
                destination
            )

        # ----------------------------------------------------
        # MOVER
        # ----------------------------------------------------

        elif action == "MV":

            if len(parts) < 3:

                print(
                    "Uso: MV <origen> <destino>"
                )

                continue

            source = parts[1]
            destination = " ".join(parts[2:])

            move_item(
                source,
                destination
            )

        # ----------------------------------------------------
        # ELIMINAR
        # ----------------------------------------------------

        elif action == "RM":

            if len(parts) < 2:

                print(
                    "Uso: RM <ruta>"
                )

                continue

            path = " ".join(parts[1:])

            remove_item(path)

        # ----------------------------------------------------
        # INFO
        # ----------------------------------------------------

        elif action == "INFO":

            if len(parts) < 2:

                print(
                    "Uso: INFO <ruta>"
                )

                continue

            path = " ".join(parts[1:])

            show_info(path)

        # ----------------------------------------------------
        # CAT
        # ----------------------------------------------------

        elif action == "CAT":

            if len(parts) < 2:

                print(
                    "Uso: CAT <archivo>"
                )

                continue

            path = " ".join(parts[1:])

            cat_file(path)

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        elif action == "SEARCH":

            if len(parts) < 2:

                print(
                    "Uso: SEARCH <texto>"
                )

                continue

            text = " ".join(parts[1:])

            search_files(text)

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
