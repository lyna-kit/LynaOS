#!/usr/bin/env python3

import os
import time
import shutil
import signal


APP_NAME = "LynaTop"
APP_VERSION = "0.3.1"

REFRESH_TIME = 2


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════════════════════════╗
║                   LynaTop 0.3.1                         ║
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
#                       /PROC
# ============================================================

def read_file(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception:

        return None


# ============================================================
#                         CPU
# ============================================================

_previous_cpu = None


def cpu_percent():

    global _previous_cpu

    content = read_file(
        "/proc/stat"
    )

    if not content:

        return 0.0

    line = content.splitlines()[0]

    parts = line.split()

    if len(parts) < 5:

        return 0.0

    try:

        values = [
            int(value)
            for value in parts[1:]
        ]

        idle = values[3]

        total = sum(values)

        if _previous_cpu is None:

            _previous_cpu = (
                total,
                idle
            )

            time.sleep(0.1)

            return cpu_percent()

        previous_total, previous_idle = (
            _previous_cpu
        )

        _previous_cpu = (
            total,
            idle
        )

        total_delta = (
            total -
            previous_total
        )

        idle_delta = (
            idle -
            previous_idle
        )

        if total_delta <= 0:

            return 0.0

        usage = (
            1 -
            idle_delta / total_delta
        ) * 100

        return max(
            0.0,
            min(
                100.0,
                usage
            )
        )

    except Exception:

        return 0.0


# ============================================================
#                          RAM
# ============================================================

def memory_stats():

    content = read_file(
        "/proc/meminfo"
    )

    if not content:

        return (
            0,
            0,
            0
        )

    values = {}

    for line in content.splitlines():

        parts = line.split()

        if len(parts) >= 2:

            key = parts[0].rstrip(":")

            try:

                value = int(parts[1])

                if len(parts) >= 3:

                    if parts[2] == "kB":

                        value *= 1024

                values[key] = value

            except ValueError:

                continue


    total = values.get(
        "MemTotal",
        0
    )

    available = values.get(
        "MemAvailable",
        values.get(
            "MemFree",
            0
        )
    )

    used = max(
        0,
        total - available
    )

    percent = (
        (used / total) * 100
        if total
        else 0
    )

    return (
        used,
        total,
        percent
    )


# ============================================================
#                          LOAD
# ============================================================

def load_average():

    try:

        load = os.getloadavg()

        return (
            f"{load[0]:.2f} "
            f"{load[1]:.2f} "
            f"{load[2]:.2f}"
        )

    except (
        AttributeError,
        OSError
    ):

        content = read_file(
            "/proc/loadavg"
        )

        if content:

            return " ".join(
                content.split()[:3]
            )

        return "N/A"


# ============================================================
#                        PROCESOS
# ============================================================

def process_count():

    try:

        return len([
            item
            for item in os.listdir(
                "/proc"
            )
            if item.isdigit()
        ])

    except Exception:

        return 0


def get_processes():

    processes = []

    try:

        entries = os.listdir(
            "/proc"
        )

    except Exception:

        return processes


    for entry in entries:

        if not entry.isdigit():

            continue

        pid = int(entry)

        status_file = (
            f"/proc/{pid}/status"
        )

        stat_file = (
            f"/proc/{pid}/stat"
        )


        name = "?"
        status = "?"
        user = "?"
        memory = 0


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        status_content = read_file(
            status_file
        )

        if status_content:

            for line in status_content.splitlines():

                if line.startswith(
                    "Name:"
                ):

                    name = line.split(
                        ":",
                        1
                    )[1].strip()


                elif line.startswith(
                    "State:"
                ):

                    state = line.split(
                        ":",
                        1
                    )[1].strip()

                    if state:

                        status = (
                            state[0]
                        )


                elif line.startswith(
                    "VmRSS:"
                ):

                    parts = line.split()

                    if len(parts) >= 2:

                        try:

                            memory = (
                                int(parts[1])
                                * 1024
                            )

                        except ValueError:

                            pass


        # ----------------------------------------------------
        # CPU
        # ----------------------------------------------------

        cpu = 0.0

        stat_content = read_file(
            stat_file
        )

        if stat_content:

            try:

                parts = stat_content.split()

                utime = int(
                    parts[13]
                )

                stime = int(
                    parts[14]
                )

                cpu = float(
                    utime + stime
                )

            except (
                IndexError,
                ValueError
            ):

                cpu = 0.0


        processes.append({

            "pid": pid,

            "name": name,

            "user": user,

            "status": status,

            "cpu": cpu,

            "memory": memory

        })


    return processes


# ============================================================
#                    MOSTRAR PROCESOS
# ============================================================

def show_processes(
    processes,
    limit
):

    processes.sort(
        key=lambda process: (
            process["cpu"],
            process["memory"]
        ),
        reverse=True
    )


    print(
        f"{'PID':>7} "
        f"{'CPU':>9} "
        f"{'MEM':>10} "
        f"{'STATUS':<8} "
        f"NAME"
    )

    print(
        "-" * 65
    )


    for process in processes[:limit]:

        name = process["name"][:30]

        status = process["status"][:7]


        print(
            f"{process['pid']:>7} "
            f"{process['cpu']:>8.0f} "
            f"{format_bytes(process['memory']):>10} "
            f"{status:<8} "
            f"{name}"
        )


# ============================================================
#                         PANTALLA
# ============================================================

def draw():

    clear()

    cpu = cpu_percent()

    used, total, memory_percent = (
        memory_stats()
    )

    load = load_average()

    processes_count = process_count()


    width, height = terminal_size()


    print(
        f"LynaTop {APP_VERSION}"
        f"   CPU: {cpu:5.1f}%"
        f"   MEM: {memory_percent:5.1f}%"
    )


    print(
        f"RAM: {format_bytes(used)} / "
        f"{format_bytes(total)}"
    )


    print(
        f"Procesos: {processes_count}"
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
        "Q = salir | "
        "R = actualizar | "
        "K <PID> = terminar"
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


    process_path = (
        f"/proc/{pid}"
    )


    if not os.path.exists(
        process_path
    ):

        print(
            "✗ El proceso ya no existe."
        )

        return


    name = "?"

    status = read_file(
        f"/proc/{pid}/status"
    )


    if status:

        for line in status.splitlines():

            if line.startswith(
                "Name:"
            ):

                name = line.split(
                    ":",
                    1
                )[1].strip()

                break


    print()

    print(
        f"⚠ Proceso: {name} "
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


    try:

        os.kill(
            pid,
            signal.SIGTERM
        )

        print(
            "✓ Señal de terminación enviada."
        )


    except ProcessLookupError:

        print(
            "✗ El proceso ya no existe."
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
#                          AYUDA
# ============================================================

def help_command():

    print("""
LynaTop 0.3.1

Monitor de procesos de LynaOS.

Comandos:

  R              Actualizar pantalla
  K <PID>        Terminar proceso
  H              Ayuda
  Q              Salir

LynaTop no requiere psutil.

Funciona utilizando la interfaz
/proc de Linux y Android/Termux.

Ejemplo:

  K 1234
""")


# ============================================================
#                           APP
# ============================================================

def run():

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

            action = (
                parts[0].upper()
            )


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


            else:

                print(
                    "Comando desconocido."
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
