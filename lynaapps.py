#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


LYNAOS_ROOT = Path(__file__).resolve().parent
APPS_DIR = LYNAOS_ROOT / "apps"


APPLICATIONS = {
    "lynacalc": (
        "lynacalc",
        "lynacalc.py"
    ),

    "lynafiles": (
        "lynafiles",
        "lynafiles.py"
    ),

    "lynasettings": (
        "lynasettings",
        "lynasettings.py"
    ),

    "lynastore": (
        "lynastore",
        "lynastore.py"
    ),

    "lynafm": (
        "lynafm",
        "lynafm.py"
    ),

    "shelly": (
        "shelly",
        "shelly.py"
    ),
}


def list_apps():

    print("""
Aplicaciones de LynaOS 0.2
──────────────────────────
""")

    for command, (_, filename) in APPLICATIONS.items():

        folder = APPLICATIONS[command][0]

        path = (
            APPS_DIR
            / folder
            / filename
        )

        status = "✓" if path.exists() else "✗"

        print(
            f"{status} {command}"
        )


def launch(app, args):

    if app not in APPLICATIONS:

        print(
            f"LynaOS: aplicación desconocida: {app}"
        )

        print(
            "Usa 'apps' para ver las aplicaciones."
        )

        return 1

    folder, filename = APPLICATIONS[app]

    application = (
        APPS_DIR
        / folder
        / filename
    )

    if not application.exists():

        print(
            f"LynaOS: no se encontró {application}"
        )

        return 1

    try:

        result = subprocess.run(
            [
                sys.executable,
                str(application),
                *args
            ]
        )

        return result.returncode

    except KeyboardInterrupt:

        return 130

    except Exception as error:

        print(
            f"LynaOS: error ejecutando {app}: {error}"
        )

        return 1


def main():

    if len(sys.argv) < 2:

        list_apps()

        return 0

    command = sys.argv[1].lower()

    if command in (
        "apps",
        "list"
    ):

        list_apps()

        return 0

    return launch(
        command,
        sys.argv[2:]
    )


if __name__ == "__main__":

    raise SystemExit(
        main()
    )
