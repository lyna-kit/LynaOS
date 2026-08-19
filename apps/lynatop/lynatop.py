#!/usr/bin/env python3

import os
import sys
import time
import shutil
import subprocess


APP_NAME = "LynaTop"
APP_VERSION = "0.3"

REFRESH_TIME = 2


# ============================================================
#                    COMPROBAR PSUTIL
# ============================================================

try:
    import psutil
except ImportError:
    psutil = None


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════════════════════════╗
║                     LynaTop 0.3                         ║
║             Monitor de procesos LynaOS                  ║
╚══════════════════════════════════════════════════════════╝
""")


# ============================================================
#                       UTILIDADES
# ============================================================

def format_bytes(value):

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    value = float(value)

    for unit in units:

        if value < 1024:
            return f"{value:.1f}{unit}"

        value /= 1024

    return f"{value:.1f}PB"


def clear():

    os.system("clear")


def terminal_size():

    try:

        return shutil.get_terminal_size(
            fallback=(100, 30)
        )

    except Exception:

        return (100, 30)


# ============================================================
#                    COMPROBAR DEPENDENCIA
# ============================================================

def check_psutil():

    if psutil is not None:
        return True

    print("""
LynaTop necesita la biblioteca psutil.

Instálala con:

  pip install psutil

Después vuelve a ejecutar LynaTop.
""")

    return False


# ============================================================
#                    INFORMACIÓN SISTEMA
# ============================================================

def system_stats():

    cpu = psutil.cpu_percent(
        interval=0.2
    )

    memory = psutil.virtual_memory()

    try:

        load = os.getloadavg()

        load_text = (
            f"{load[0]:.2f} "
            f"{load[1]:.2f} "
            f"{load[2]:.2f}"
        )

    except (AttributeError, OSError):

        load_text = "N/A"

    process_count = len(
        psutil.pids()
    )

    return (
        cpu,
        memory,
        load_text,
        process_count
    )


# ============================================================
#                     PROCESOS
# ============================================================

def get_processes():

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "username",
            "status",
            "memory_info"
        ]
    ):

        try:

            info = process.info

            memory_info = info.get(
                "memory_info"
            )

            rss = (
                memory_info.rss
                if memory_info
                else 0
            )

            cpu = process.cpu_percent(
                interval=None
            )

            processes.append({
                "pid": info.get(
                    "pid",
                    0
                ),

                "name": info.get(
                    "name",
                    "?"
                ) or "?",

                "user": info.get(
                    "username",
                    "?"
                ) or "?",

                "status": info.get(
                    "status",
                    "?"
                ) or "?",

                "cpu": cpu,

                "memory": rss
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            continue

        except Exception:

            continue

    return processes


# ============================================================
#                     MOSTRAR PROCESOS
# ============================================================

def show_processes(processes, limit):

    processes.sort(
        key=lambda process: (
            process["cpu"],
            process["memory"]
        ),
        reverse=True
    )

    print(
        f"{'PID':>7} "
        f"{'CPU%':>7} "
        f"{'MEM':>10} "
        f"{'STATUS':<12} "
        f"{'USER':<15} "
        f"NAME"
    )

    print(
        "-" * 80
    )

    for process in processes[:limit]:

        name = process["name"][:25]
        user = process["user"][:14]
        status = process["status"][:11]

        print(
            f"{process['pid']:>7} "
            f"{process['cpu']:>6.1f} "
            f"{format_bytes(process['memory']):>10} "
            f"{status:<12} "
            f"{user:<15} "
            f"{name}"
        )


# ============================================================
#                         PANTALLA
# ============================================================

def draw():

    clear()

    cpu, memory, load, process_count = (
        system_stats()
    )

    width, height = terminal_size()

    print(
        f"LynaTop {APP_VERSION}"
        f"   CPU: {cpu:5.1f}%"
        f"   MEM: {memory.percent:5.1f}%"
    )

    print(
        f"RAM: {format_bytes(memory.used)} / "
        f"{format_bytes(memory.total)}"
    )

    print(
        f"Procesos: {process_count}"
        f"   Load: {load}"
    )

    print()

    processes = get_processes()

    limit = max(
        5,
        height - 10
    )

    show_processes(
        processes,
        limit
    )

    print()
    print(
        "Q = salir | R = actualizar | "
        "K <PID> = terminar proceso"
    )


# ============================================================
#                    TERMINAR PROCESO
# ============================================================

def kill_process(pid):

    try:

        pid = int(pid)

    except ValueError:

        print(
            "PID inválido."
        )

        return

    try:

        process = psutil.Process(
            pid
        )

        print()
        print(
            f"⚠ Proceso: {process.name()} "
            f"(PID {pid})"
        )

        confirmation = input(
            "¿Terminar proceso? [s/N]: "
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

        process.terminate()

        try:

            process.wait(
                timeout=3
            )

            print(
                "✓ Proceso terminado."
            )

        except psutil.TimeoutExpired:

            print(
                "El proceso no respondió."
            )

            force = input(
                "¿Forzar terminación? [s/N]: "
            ).strip().lower()

            if force in (
                "s",
                "si",
                "sí",
                "y",
                "yes"
            ):

                process.kill()

                print(
                    "✓ Proceso terminado."
                )

    except psutil.NoSuchProcess:

        print(
            "✗ El proceso ya no existe."
        )

    except psutil.AccessDenied:

        print(
            "✗ Permiso denegado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )


# ============================================================
#                         AYUDA
# ============================================================

def help_command():

    print("""
LynaTop 0.3

Monitor de procesos de LynaOS.

Comandos:

  R              Actualizar pantalla
  K <PID>        Terminar proceso
  H              Ayuda
  Q              Salir

La pantalla se actualiza automáticamente.

Ejemplo:

  K 1234
""")


# ============================================================
#                           APP
# ============================================================

def run():

    if not check_psutil():
        return

    banner()

    time.sleep(1)

    while True:

        try:

            draw()

            command = input(
                "\nlynatop> "
            ).strip()

            if not command:

                continue

            parts = command.split()

            action = parts[0].upper()

            if action in (
                "Q",
                "EXIT"
            ):

                print(
                    "Saliendo de LynaTop..."
                )

                break

            elif action in (
                "R",
                "REFRESH"
            ):

                continue

            elif action in (
                "H",
                "HELP"
            ):

                help_command()

                input(
                    "\nENTER para continuar..."
                )

            elif action == "K":

                if len(parts) < 2:

                    print(
                        "Uso: K <PID>"
                    )

                    input(
                        "\nENTER para continuar..."
                    )

                    continue

                kill_process(
                    parts[1]
                )

                input(
                    "\nENTER para continuar..."
                )

        except KeyboardInterrupt:

            print()

            break

        except EOFError:

            print()

            break

        except Exception as error:

            print(
                f"Error: {error}"
            )

            time.sleep(2)


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":
    run()
