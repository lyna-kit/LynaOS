#!/usr/bin/env python3

from pathlib import Path


# ============================================================
#                    LynaOS VERSION SYSTEM
# ============================================================

LYNAOS_ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = LYNAOS_ROOT / "version.cfg"


DEFAULT_VERSION = {
    "MAJOR": "0",
    "MINOR": "2",
    "PATCH": "0",
    "CHANNEL": "dev",
    "BUILD": "1"
}


def load_version():

    version = DEFAULT_VERSION.copy()

    if not VERSION_FILE.exists():

        return version

    try:

        with open(
            VERSION_FILE,
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

                if key in version:

                    version[key] = value

    except Exception:

        return DEFAULT_VERSION.copy()

    return version


def version_string():

    version = load_version()

    base = (
        f"{version['MAJOR']}."
        f"{version['MINOR']}."
        f"{version['PATCH']}"
    )

    channel = version["CHANNEL"]

    if channel:

        return (
            f"{base}-{channel}"
        )

    return base


def build_string():

    version = load_version()

    return (
        f"Build {version['BUILD']}"
    )


def full_version():

    return (
        f"LynaOS {version_string()} "
        f"({build_string()})"
    )


def version_tuple():

    version = load_version()

    return (
        int(version["MAJOR"]),
        int(version["MINOR"]),
        int(version["PATCH"])
    )


def is_stable():

    return (
        load_version()["CHANNEL"]
        == "stable"
    )


if __name__ == "__main__":

    print(
        full_version()
    )
