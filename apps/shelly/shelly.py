#!/usr/bin/env python3

import os
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser


APP_NAME = "Shelly"
APP_VERSION = "0.1"

current_url = ""


# ============================================================
#                        HTML PARSER
# ============================================================

class ShellyParser(HTMLParser):

    def __init__(self):

        super().__init__()

        self.output = []
        self.links = []
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag, attrs):

        tag = tag.lower()

        if tag in ("script", "style"):
            self.in_script = True
            self.in_style = tag == "style"
            return

        if tag == "br":
            self.output.append("\n")

        elif tag in ("p", "div"):
            self.output.append("\n")

        elif tag in ("h1", "h2", "h3"):

            self.output.append(
                "\n\n### "
            )

        elif tag == "li":

            self.output.append(
                "\n* "
            )

        elif tag == "a":

            attributes = dict(attrs)
            href = attributes.get("href")

            if href:

                self.links.append(href)

                number = len(self.links)

                self.output.append(
                    f" [{number}]"
                )

    def handle_endtag(self, tag):

        tag = tag.lower()

        if tag == "script":

            self.in_script = False

        elif tag == "style":

            self.in_style = False

        elif tag in ("p", "div"):

            self.output.append("\n")

    def handle_data(self, data):

        if self.in_script or self.in_style:
            return

        text = " ".join(
            data.split()
        )

        if text:
            self.output.append(
                text + " "
            )

    def get_text(self):

        text = "".join(
            self.output
        )

        text = re.sub(
            r"\n\s*\n\s*\n+",
            "\n\n",
            text
        )

        return text.strip()


# ============================================================
#                         DESCARGAR
# ============================================================

def fetch(url):

    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                    "Shelly/0.1 LynaOS"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            if "text/html" not in content_type:

                print(
                    f"Shelly: contenido no HTML ({content_type})"
                )

                return None

            charset = response.headers.get_content_charset()

            if not charset:
                charset = "utf-8"

            data = response.read()

            return (
                data.decode(
                    charset,
                    errors="replace"
                ),
                response.geturl()
            )

    except Exception as error:

        print(
            f"Shelly: error de conexión: {error}"
        )

        return None


# ============================================================
#                          MOSTRAR
# ============================================================

def browse(url):

    global current_url

    if not url.startswith(
        ("http://", "https://")
    ):

        url = (
            "https://"
            + url
        )

    result = fetch(url)

    if result is None:
        return

    html, final_url = result

    parser = ShellyParser()

    parser.feed(html)

    current_url = final_url

    print()
    print(
        "═" * 70
    )

    print(
        f"Shelly — {current_url}"
    )

    print(
        "═" * 70
    )

    print()

    text = parser.get_text()

    if text:

        print(text)

    else:

        print(
            "(La página no contiene texto visible.)"
        )

    print()

    if parser.links:

        print(
            "Enlaces:"
        )

        for number, link in enumerate(
            parser.links,
            start=1
        ):

            absolute = urllib.parse.urljoin(
                current_url,
                link
            )

            print(
                f"  [{number}] {absolute}"
            )

    print(
        "═" * 70
    )


# ============================================================
#                          AYUDA
# ============================================================

def help_command():

    print("""
Shelly 0.1 — navegador de texto

Comandos:

  open <URL>      Abrir una página
  back            Volver
  links           Mostrar enlaces
  go <número>     Abrir un enlace
  refresh         Recargar página
  clear           Limpiar pantalla
  about           Información
  help            Ayuda
  exit            Salir

Ejemplos:

  open https://example.com
  open https://www.wikipedia.org
""")


# ============================================================
#                          ABOUT
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Navegador web de texto oficial de LynaOS.

Motor: Python urllib + HTMLParser
Interfaz: terminal
Sistema: LynaOS
""")


# ============================================================
#                          ENLACES
# ============================================================

last_links = []


def show_links():

    global last_links

    if not current_url:

        print(
            "Shelly: no hay ninguna página abierta."
        )

        return

    result = fetch(current_url)

    if result is None:
        return

    html, final_url = result

    parser = ShellyParser()

    parser.feed(html)

    last_links = [
        urllib.parse.urljoin(
            final_url,
            link
        )
        for link in parser.links
    ]

    if not last_links:

        print(
            "Shelly: esta página no tiene enlaces."
        )

        return

    for number, link in enumerate(
        last_links,
        start=1
    ):

        print(
            f"[{number}] {link}"
        )


# ============================================================
#                         APLICACIÓN
# ============================================================

def run():

    global current_url
    global last_links

    print(f"""
╔══════════════════════════════════════╗
║            Shelly {APP_VERSION}             ║
║       Navegador de texto LynaOS     ║
╚══════════════════════════════════════╝

Escribe HELP para obtener ayuda.
""")

    while True:

        try:

            command = input(
                "shelly> "
            ).strip()

            if not command:
                continue

            parts = command.split(
                maxsplit=1
            )

            cmd = parts[0].lower()

            argument = (
                parts[1].strip()
                if len(parts) > 1
                else ""
            )

            # ------------------------------------------------
            # EXIT
            # ------------------------------------------------

            if cmd in ("exit", "quit"):

                print(
                    "Saliendo de Shelly..."
                )

                break

            # ------------------------------------------------
            # OPEN
            # ------------------------------------------------

            elif cmd == "open":

                if not argument:

                    print(
                        "Uso: open <URL>"
                    )

                else:

                    browse(argument)

            # ------------------------------------------------
            # LINKS
            # ------------------------------------------------

            elif cmd == "links":

                show_links()

            # ------------------------------------------------
            # GO
            # ------------------------------------------------

            elif cmd == "go":

                if not argument:

                    print(
                        "Uso: go <número>"
                    )

                    continue

                try:

                    number = int(
                        argument
                    )

                    if (
                        number < 1
                        or number > len(last_links)
                    ):

                        print(
                            "Enlace inexistente."
                        )

                    else:

                        browse(
                            last_links[
                                number - 1
                            ]
                        )

                except ValueError:

                    print(
                        "Número inválido."
                    )

            # ------------------------------------------------
            # REFRESH
            # ------------------------------------------------

            elif cmd == "refresh":

                if current_url:

                    browse(
                        current_url
                    )

                else:

                    print(
                        "No hay ninguna página abierta."
                    )

            # ------------------------------------------------
            # BACK
            # ------------------------------------------------

            elif cmd == "back":

                print(
                    "Historial de navegación disponible "
                    "en una versión futura de Shelly."
                )

            # ------------------------------------------------
            # HELP
            # ------------------------------------------------

            elif cmd in ("help", "h"):

                help_command()

            # ------------------------------------------------
            # ABOUT
            # ------------------------------------------------

            elif cmd == "about":

                about()

            # ------------------------------------------------
            # CLEAR
            # ------------------------------------------------

            elif cmd == "clear":

                os.system("clear")

            else:

                print(
                    "Shelly: comando desconocido."
                )

                print(
                    "Escribe HELP para ver los comandos."
                )

        except KeyboardInterrupt:

            print()

            break

        except EOFError:

            break


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":
    run()
