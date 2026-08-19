#!/usr/bin/env python3

import os
import time
from datetime import datetime


APP_NAME = "LynaClock"
APP_VERSION = "0.3"


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════════════════════════╗
║                    LynaClock 0.3                        ║
║                 Reloj de LynaOS                         ║
╚══════════════════════════════════════════════════════════╝
""")


# ============================================================
#                         AYUDA
# ============================================================

def help_command():

    print("""
LynaClock 0.3

Comandos:

  START       Iniciar reloj
  NOW         Mostrar hora actual
  DATE        Mostrar fecha actual
  ABOUT       Información
  CLEAR       Limpiar pantalla
  H           Ayuda
  Q           Salir

El reloj se actualiza automáticamente cuando está activo.
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
#                      MOSTRAR HORA
# ============================================================

def show_now():

    now = datetime.now()

    print()
    print(
        f"Hora: {now.strftime('%H:%M:%S')}"
    )

    print(
        f"Fecha: {get_date()}"
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
║                    LynaClock 0.3                        ║
╚══════════════════════════════════════════════════════════╝
""")

            print()
            print(
                f"                    {now.strftime('%H:%M:%S')}"
            )

            print()
            print(
                f"              {get_date()}"
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
  • Actualización cada segundo
  • Interfaz de terminal
""")


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

        action = command.upper()

        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        if action in (
            "Q",
            "EXIT"
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
        # ABOUT
        # ----------------------------------------------------

        elif action == "ABOUT":

            about()

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        elif action == "CLEAR":

            clear()

        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        elif action in (
            "H",
            "HELP"
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
