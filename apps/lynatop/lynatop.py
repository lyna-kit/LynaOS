#!/usr/bin/env python3

import os
import signal
import shutil
import time


APP_NAME = "LynaTop"
APP_VERSION = "0.4"

REFRESH_TIME = 2


# ============================================================
#                         ESTADO
# ============================================================

_previous_cpu = None
_process_cpu = {}


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════════════════════════╗
║                    LynaTop 0.4                          ║
║              Monitor de LynaOS                          ║
╚══════════════════════════════════════════════════════════╝
""")


# ============================================================
#                       UTILIDADES
# ============================================================

def format_bytes(value):

    units = (
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    )

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
#                           CPU
# ============================================================

def read_cpu_times():

    content = read_file(
        "/proc/stat"
    )

    if not content:

        return None

    try:

        line = content.splitlines()[0]
        parts = line.split()

        if not parts or parts[0] != "cpu":

            return None

        values = [
            int(value)
            for value in parts[1:]
        ]

        if len(values) < 4:

            return None

        total = sum(values)
        idle = values[3]

        return total, idle

    except (
        ValueError,
        IndexError
    ):

        return None


def cpu_percent():

    global _previous_cpu

    current = read_cpu_times()

    if current is None:

        return 0.0

    if _previous_cpu is None:

        _previous_cpu = current

        return 0.0

    previous_total, previous_idle = (
        _previous_cpu
    )

    current_total, current_idle = current

    total_delta = (
        current_total -
        previous_total
    )

    idle_delta = (
        current_idle -
        previous_idle
    )

    _previous_cpu = current

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


# ============================================================
#                          RAM
# ============================================================

def memory_stats():

    content = read_file(
        "/proc/meminfo"
    )

    if not content:

        return 0, 0, 0

    values = {}

    for line in content.splitlines():

        parts = line.split()

        if len(parts) < 2:

            continue

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
        used / total * 100
        if total
        else 0.0
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
#                       PROCESOS
# ============================================================

def process_count():

    try:

        return sum(
            1
            for item in os.listdir("/proc")
            if item.isdigit()
        )

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

        status_content = read_file(
            f"/proc/{pid}/status"
        )

        stat_content = read_file(
            f"/proc/{pid}/stat"
        )

        if not status_content:

            continue

        name = "?"
        status = "?"
        memory = 0

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        for line in status_content.splitlines():

            if line.startswith("Name:"):

                name = line.split(
                    ":",
                    1
                )[1].strip()

            elif line.startswith("State:"):

                state = line.split(
                    ":",
                    1
                )[1].strip()

                if state:

                    status = state[0]

            elif line.startswith("VmRSS:"):

                parts = line.split()

                if len(parts) >= 2:

                    try:

                        memory = (
                            int(parts[1]) *
                            1024
                        )

                    except ValueError:

                        pass

        # ----------------------------------------------------
        # CPU DEL PROCESO
        # ----------------------------------------------------

        cpu_time = 0

        if stat_content:

            try:

                parts = stat_content.split()

                utime = int(parts[13])
                stime = int(parts[14])

                cpu_time = (
                    utime +
                    stime
                )

            except (
                IndexError,
                ValueError
            ):

                cpu_time = 0

        previous = _process_cpu.get(
            pid
        )

        _process_cpu[pid] = (
            cpu_time,
            time.monotonic()
        )

        cpu = 0.0

        if previous is not None:

            previous_time, previous_stamp = (
                previous
            )

            elapsed = (
                time.monotonic() -
                previous_stamp
            )

            delta = (
                cpu_time -
                previous_time
            )

            if elapsed > 0 and delta >= 0:

                try:

                    clock_ticks = os.sysconf(
                        os.sysconf_names[
                            "SC_CLK_TCK"
                        ]
                    )

                except (
                    ValueError,
                    KeyError,
                    OSError
                ):

                    clock_ticks = 100

                cpu = (
                    delta /
                    clock_ticks /
                    elapsed
                ) * 100

        processes.append({
            "pid": pid,
            "name": name,
            "status": status,
            "cpu": cpu,
            "memory": memory
        })

    # Limpiar procesos desaparecidos.

    active_pids = {
        process["pid"]
        for process in processes
    }

    for pid in list(_process_cpu):

        if pid not in active_pids:

            del _process_cpu[pid]

    return processes


# ============================================================
#                    MOSTRAR PROCESOS
# ============================================================

def show_processes(
    processes,
    limit,
    width
):

    processes.sort(
        key=lambda process: (
            process["cpu"],
            process["memory"]
        ),
        reverse=True
    )

    name_width = max(
        15,
        min(
            32,
            width - 42
        )
    )

    print(
        f"{'PID':>7} "
        f"{'CPU':>7} "
        f"{'MEM':>10} "
        f"{'S':<2} "
        f"{'NAME':<{name_width}}"
    )

    print(
        "-" * min(
            width,
            7 + 1 + 7 + 1 + 10 + 1 + 2 + 1 + name_width
        )
    )

    for process in processes[:limit]:

        name = process["name"][
            :name_width
        ]

        status = process["status"][:1]

        print(
            f"{process['pid']:>7} "
            f"{process['cpu']:>6.1f}% "
            f"{format_bytes(process['memory']):>10} "
            f"{status:<2} "
            f"{name:<{name_width}}"
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
    )

    print(
        f"CPU: {cpu:5.1f}%"
        f"    RAM: {memory_percent:5.1f}%"
    )

    print(
        f"RAM: {format_bytes(used)} / "
        f"{format_bytes(total)}"
    )

    print(
        f"Procesos: {processes_count}"
        f"    Load: {load}"
    )

    print()

    processes = get_processes()

    limit = max(
        5,
        height - 11
    )

    show_processes(
        processes,
        limit,
        width
    )

    print()

    print(
        "R = actualizar | "
        "K <PID> = terminar | "
        "H = ayuda | "
        "Q = salir"
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

    if pid <= 0:

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

            if line.startswith("Name:"):

                name = line.split(
                    ":",
                    1
                )[1].strip()

                break

    print()

    print(
        f"⚠ Proceso: {name}"
        f" (PID {pid})"
    )

    print(
        "Esta acción enviará SIGTERM."
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
            "✓ Señal SIGTERM enviada."
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
LynaTop 0.4

Monitor de rendimiento y procesos de LynaOS.

Información:

  • Uso global de CPU
  • Uso de RAM
  • RAM total y disponible
  • Load average
  • Número de procesos
  • CPU individual de procesos
  • Memoria individual de procesos

Comandos:

  R              Actualizar
  K <PID>        Terminar proceso
  H              Mostrar ayuda
  Q              Salir

LynaTop utiliza /proc de Linux/Android
y no necesita psutil.

Ejemplo:

  K 1234
""")


# ============================================================
#                           VERSION
# ============================================================

def version_command():

    print(
        f"{APP_NAME} {APP_VERSION}"
    )

    print(
        "Monitor de rendimiento de LynaOS"
    )

    print(
        "Backend: /proc"
    )


# ============================================================
#                            APP
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

            action = parts[0].upper()

            if action in (
                "Q",
                "EXIT",
                "QUIT"
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

                clear()

                help_command()

                input(
                    "\nENTER para continuar..."
                )

            elif action in (
                "V",
                "VERSION"
            ):

                clear()

                version_command()

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
            print(
                "Saliendo de LynaTop..."
            )

            break

        except EOFError:

            print()
            print(
                "Saliendo de LynaTop..."
            )

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
