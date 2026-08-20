#!/usr/bin/env python3

import os
import time
from datetime import datetime, timezone


APP_NAME = "LynaClock"
APP_VERSION = "0.4"

TWELVE_HOUR = False
SHOW_SECONDS = True


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════════════════════════╗
║                    LynaClock 0.4                        ║
║                  Reloj de LynaOS                        ║
╚══════════════════════════════════════════════════════════╝

Escribe H para ver la ayuda.
""")


# ============================================================
#                         AYUDA
# ============================================================

def help_command():

    print("""
LynaClock 0.4

Comandos:

  START          Iniciar reloj en tiempo real
  NOW            Mostrar hora y fecha actuales
  DATE           Mostrar fecha actual
  UTC            Mostrar hora UTC
  12H            Usar formato de 12 horas
  24H            Usar formato de 24 horas
  SECONDS ON     Mostrar segundos
  SECONDS OFF    Ocultar segundos
  VERSION        Mostrar versión
  ABOUT          Información
  CLEAR          Limpiar pantalla
  H              Ayuda
  Q              Salir

Durante START:

  Ctrl+C        Detener el reloj

El formato de hora y la opción de segundos
se conservan mientras LynaClock está abierto.
""")


# ============================================================
#                       OBTENER FECHA
# ============================================================

def get_date():

    now = datetime.now()

    days = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo"
    ]

    months = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre"
    ]

    day_name = days[
        now.weekday()
    ]

    month_name = months[
        now.month - 1
    ]

    return (
        f"{day_name}, "
        f"{now.day} de "
        f"{month_name} de "
        f"{now.year}"
    )


# ============================================================
#                    FORMATO DE HORA
# ============================================================

def format_time(now=None):

    if now is None:

        now = datetime.now()

    if TWELVE_HOUR:

        if SHOW_SECONDS:

            return now.strftime(
                "%I:%M:%S %p"
            )

        return now.strftime(
            "%I:%M %p"
        )

    if SHOW_SECONDS:

        return now.strftime(
            "%H:%M:%S"
        )

    return now.strftime(
        "%H:%M"
    )


# ============================================================
#                      MOSTRAR HORA
# ============================================================

def show_now():

    now = datetime.now()

    print()
    print(
        f"Hora: {format_time(now)}"
    )

    print(
        f"Fecha: {get_date()}"
    )

    print()


# ============================================================
#                       HORA UTC
# ============================================================

def show_utc():

    now = datetime.now(
        timezone.utc
    )

    if TWELVE_HOUR:

        if SHOW_SECONDS:

            formatted = now.strftime(
                "%I:%M:%S %p"
            )

        else:

            formatted = now.strftime(
                "%I:%M %p"
            )

    else:

        if SHOW_SECONDS:

            formatted = now.strftime(
                "%H:%M:%S"
            )

        else:

            formatted = now.strftime(
                "%H:%M"
            )

    print()
    print(
        f"UTC: {formatted}"
    )
    print()


# ============================================================
#                    RELOJ EN TIEMPO REAL
# ============================================================

def start_clock():

    try:

        while True:

            now = datetime.now()

            clear()

            print("""
╔══════════════════════════════════════════════════════════╗
║                    LynaClock 0.4                        ║
╚══════════════════════════════════════════════════════════╝
""")

            print()
            print(
                f"                    {format_time(now)}"
            )

            print()
            print(
                f"              {get_date()}"
            )

            print()

            format_mode = (
                "12 horas"
                if TWELVE_HOUR
                else "24 horas"
            )

            seconds_mode = (
                "ON"
                if SHOW_SECONDS
                else "OFF"
            )

            print(
                f"        Formato: {format_mode}"
            )

            print(
                f"        Segundos: {seconds_mode}"
            )

            print()
            print(
                "              Ctrl+C para salir"
            )

            time.sleep(1)

    except KeyboardInterrupt:

        clear()

        print(
            "LynaClock detenido."
        )

        print()


# ============================================================
#                         LIMPIAR
# ============================================================

def clear():

    os.system("clear")


# ============================================================
#                           ABOUT
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Reloj oficial de LynaOS.

Funciones:

  • Hora en tiempo real
  • Fecha
  • Día de la semana
  • Formato de 12/24 horas
  • Mostrar u ocultar segundos
  • Hora UTC
  • Actualización cada segundo
  • Interfaz de terminal
""")


# ============================================================
#                         VERSION
# ============================================================

def version():

    print()
    print(
        f"{APP_NAME} {APP_VERSION}"
    )
    print(
        "Reloj de LynaOS"
    )
    print()


# ============================================================
#                      CAMBIAR FORMATO
# ============================================================

def set_time_format(use_12_hour):

    global TWELVE_HOUR

    TWELVE_HOUR = use_12_hour

    if TWELVE_HOUR:

        print(
            "✓ Formato cambiado a 12 horas."
        )

    else:

        print(
            "✓ Formato cambiado a 24 horas."
        )


# ============================================================
#                     SEGUNDOS ON/OFF
# ============================================================

def set_seconds(enabled):

    global SHOW_SECONDS

    SHOW_SECONDS = enabled

    if SHOW_SECONDS:

        print(
            "✓ Segundos activados."
        )

    else:

        print(
            "✓ Segundos ocultos."
        )


# ============================================================
#                            APP
# ============================================================

def run():

    banner()

    while True:

        try:

            command = input(
                "lynaclock> "
            ).strip()

        except KeyboardInterrupt:

            print()

            print(
                "Saliendo de LynaClock..."
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
            "EXIT",
            "QUIT"
        ):

            print(
                "Saliendo de LynaClock..."
            )

            break

        # ----------------------------------------------------
        # START
        # ----------------------------------------------------

        elif action in (
            "START",
            "CLOCK"
        ):

            start_clock()

        # ----------------------------------------------------
        # NOW
        # ----------------------------------------------------

        elif action == "NOW":

            show_now()

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        elif action == "DATE":

            print()
            print(
                get_date()
            )
            print()

        # ----------------------------------------------------
        # UTC
        # ----------------------------------------------------

        elif action == "UTC":

            show_utc()

        # ----------------------------------------------------
        # 12H
        # ----------------------------------------------------

        elif action == "12H":

            set_time_format(
                True
            )

        # ----------------------------------------------------
        # 24H
        # ----------------------------------------------------

        elif action == "24H":

            set_time_format(
                False
            )

        # ----------------------------------------------------
        # SECONDS
        # ----------------------------------------------------

        elif action == "SECONDS":

            if len(parts) < 2:

                print(
                    "Uso: SECONDS ON/OFF"
                )

                continue

            value = parts[1].upper()

            if value == "ON":

                set_seconds(
                    True
                )

            elif value == "OFF":

                set_seconds(
                    False
                )

            else:

                print(
                    "Uso: SECONDS ON/OFF"
                )

        # ----------------------------------------------------
        # VERSION
        # ----------------------------------------------------

        elif action in (
            "VERSION",
            "--VERSION",
            "-V"
        ):

            version()

        # ----------------------------------------------------
        # ABOUT
        # ----------------------------------------------------

        elif action == "ABOUT":

            about()

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        elif action in (
            "CLEAR",
            "CLS"
        ):

            clear()

        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        elif action in (
            "H",
            "HELP",
            "?"
        ):

            help_command()

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
