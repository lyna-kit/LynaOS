#!/usr/bin/env python3

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
#                     LynaOS BUILD SYSTEM
# ============================================================

LYNAOS_ROOT = Path(__file__).resolve().parents[1]

VERSION_FILE = LYNAOS_ROOT / "version.cfg"
CHANGELOG_FILE = LYNAOS_ROOT / "system" / "changelog.json"


# ============================================================
#                       VERSION
# ============================================================

def load_version():

    version = {}

    if not VERSION_FILE.exists():

        print(
            "ERROR: version.cfg no existe."
        )

        sys.exit(1)

    with open(
        VERSION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if (
                not line
                or line.startswith("#")
                or "=" not in line
            ):
                continue

            key, value = line.split(
                "=",
                1
            )

            version[key.strip()] = value.strip()

    return version


# ============================================================
#                    GUARDAR VERSION
# ============================================================

def save_version(version):

    lines = [
        f"MAJOR={version.get('MAJOR', '0')}",
        f"MINOR={version.get('MINOR', '0')}",
        f"PATCH={version.get('PATCH', '0')}",
        f"CHANNEL={version.get('CHANNEL', 'dev')}",
        f"BUILD={version.get('BUILD', '1')}"
    ]

    if "CODENAME" in version:
        lines.append(
            f"CODENAME={version['CODENAME']}"
        )

    if "DATE" in version:
        lines.append(
            f"DATE={version['DATE']}"
        )

    if "MIN_UPDATE_FROM" in version:
        lines.append(
            f"MIN_UPDATE_FROM={version['MIN_UPDATE_FROM']}"
        )

    with open(
        VERSION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(lines)
            + "\n"
        )


# ============================================================
#                       CHANGELOG
# ============================================================

def load_changelog():

    if not CHANGELOG_FILE.exists():

        return {}

    try:

        with open(
            CHANGELOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError:

        print(
            "ERROR: changelog.json no es válido."
        )

        sys.exit(1)


def save_changelog(changelog):

    with open(
        CHANGELOG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            changelog,
            file,
            indent=4,
            ensure_ascii=False
        )

        file.write("\n")


# ============================================================
#                       INFORMACIÓN
# ============================================================

def version_string(version):

    return (
        f"{version.get('MAJOR', '0')}."
        f"{version.get('MINOR', '0')}."
        f"{version.get('PATCH', '0')}"
    )


def build_string(version):

    return (
        f"Build {version.get('BUILD', '1')}"
    )


# ============================================================
#                         BACKUP
# ============================================================

def create_backup():

    backup_dir = (
        LYNAOS_ROOT
        / "system"
        / "backups"
    )

    backup_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (
        backup_dir
        / f"version_{timestamp}.cfg"
    )

    shutil.copy2(
        VERSION_FILE,
        backup_file
    )

    return backup_file


# ============================================================
#                     CREAR NUEVA BUILD
# ============================================================

def create_build():

    version = load_version()

    old_build = int(
        version.get(
            "BUILD",
            "1"
        )
    )

    new_build = old_build + 1

    version["BUILD"] = str(
        new_build
    )

    version["DATE"] = (
        datetime.now().strftime(
            "%Y-%m-%d"
        )
    )

    backup = create_backup()

    save_version(
        version
    )

    changelog = load_changelog()

    current_version = version_string(
        version
    )

    if current_version not in changelog:

        changelog[current_version] = {
            "codename": version.get(
                "CODENAME",
                ""
            ),
            "channel": version.get(
                "CHANNEL",
                "dev"
            ),
            "build": new_build,
            "date": version["DATE"],
            "changes": []
        }

    else:

        changelog[current_version][
            "build"
        ] = new_build

        changelog[current_version][
            "date"
        ] = version["DATE"]

    save_changelog(
        changelog
    )

    print()
    print(
        "╔══════════════════════════════════════╗"
    )
    print(
        "║          LynaOS Build System         ║"
    )
    print(
        "╚══════════════════════════════════════╝"
    )
    print()

    print(
        f"Versión : {current_version}"
    )

    print(
        f"Canal   : {version.get('CHANNEL', 'dev')}"
    )

    print(
        f"Build   : {new_build}"
    )

    print(
        f"Fecha   : {version['DATE']}"
    )

    print()
    print(
        f"✓ Nueva build creada: "
        f"LynaOS {current_version} "
        f"(Build {new_build})"
    )

    print()
    print(
        f"Backup: {backup}"
    )


# ============================================================
#                          INFO
# ============================================================

def show_info():

    version = load_version()

    print()
    print(
        f"LynaOS {version_string(version)}"
    )

    print(
        f"Canal: {version.get('CHANNEL', 'dev')}"
    )

    print(
        f"Build: {version.get('BUILD', '1')}"
    )

    print(
        f"Fecha: {version.get('DATE', 'N/A')}"
    )

    print(
        f"Codename: {version.get('CODENAME', 'N/A')}"
    )


# ============================================================
#                           HELP
# ============================================================

def help_command():

    print("""
LynaOS Build System

Uso:

  python system/build.py build
      Crear una nueva build.

  python system/build.py info
      Mostrar información de la build actual.

  python system/build.py help
      Mostrar esta ayuda.
""")


# ============================================================
#                            MAIN
# ============================================================

def main():

    if len(sys.argv) < 2:

        help_command()

        return

    command = sys.argv[1].lower()

    if command == "build":

        create_build()

    elif command == "info":

        show_info()

    elif command in (
        "help",
        "-h",
        "--help"
    ):

        help_command()

    else:

        print(
            f"Comando desconocido: {command}"
        )

        help_command()


if __name__ == "__main__":

    main()
