#!/usr/bin/env python3

import os
import re
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse


APP_NAME = "Shelly"
APP_VERSION = "0.3"

USER_AGENT = "Shelly/0.3 LynaOS"


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════╗
║             Shelly 0.3               ║
║        Navegador de texto            ║
╚══════════════════════════════════════╝

Comandos:

  OPEN <URL>       Abrir página
  LINKS            Mostrar enlaces
  BACK             Página anterior
  FORWARD          Página siguiente
  SAVE <archivo>   Guardar página
  CLEAR            Limpiar pantalla
  ABOUT            Información
  H                Ayuda
  Q                Salir
""")


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print("""
Shelly 0.3

Navegación:

  OPEN <URL>       Abrir una página web
  LINKS            Mostrar enlaces encontrados
  BACK             Volver a la página anterior
  FORWARD          Avanzar en el historial

Archivos:

  SAVE <archivo>   Guardar el contenido actual

Sistema:

  CLEAR            Limpiar pantalla
  ABOUT            Información
  H                Ayuda
  Q                Salir

Ejemplos:

  OPEN https://example.com
  LINKS
  SAVE pagina.txt
""")


# ============================================================
#                    LIMPIAR HTML
# ============================================================

def html_to_text(html):

    # Eliminar scripts y estilos.

    html = re.sub(
        r"<script\b[^>]*>.*?</script>",
        " ",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    html = re.sub(
        r"<style\b[^>]*>.*?</style>",
        " ",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Separadores visuales.

    html = re.sub(
        r"<br\s*/?>",
        "\n",
        html,
        flags=re.IGNORECASE
    )

    html = re.sub(
        r"</p\s*>",
        "\n\n",
        html,
        flags=re.IGNORECASE
    )

    html = re.sub(
        r"</div\s*>",
        "\n",
        html,
        flags=re.IGNORECASE
    )

    html = re.sub(
        r"</h[1-6]\s*>",
        "\n\n",
        html,
        flags=re.IGNORECASE
    )

    # Eliminar etiquetas.

    html = re.sub(
        r"<[^>]+>",
        " ",
        html
    )

    # Decodificar entidades HTML.

    text = unescape(html)

    # Normalizar espacios.

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
#                         ENLACES
# ============================================================

def extract_links(html, base_url):

    links = []

    pattern = re.compile(
        r'<a\s+[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        re.IGNORECASE | re.DOTALL
    )

    for match in pattern.finditer(html):

        href = unescape(
            match.group(1).strip()
        )

        label = html_to_text(
            match.group(2)
        )

        if not href:
            continue

        absolute = urljoin(
            base_url,
            href
        )

        parsed = urlparse(
            absolute
        )

        if parsed.scheme not in (
            "http",
            "https"
        ):

            continue

        links.append(
            (
                label or absolute,
                absolute
            )
        )

    return links


# ============================================================
#                        DESCARGAR
# ============================================================

def fetch_page(url):

    if not url.startswith(
        ("http://", "https://")
    ):

        url = "https://" + url

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            final_url = response.geturl()
            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            data = response.read()

            charset = response.headers.get_content_charset()

            if not charset:

                charset = "utf-8"

            try:

                html = data.decode(
                    charset,
                    errors="replace"
                )

            except LookupError:

                html = data.decode(
                    "utf-8",
                    errors="replace"
                )

            return (
                final_url,
                content_type,
                html
            )

    except urllib.error.HTTPError as error:

        print(
            f"✗ HTTP {error.code}: {error.reason}"
        )

    except urllib.error.URLError as error:

        print(
            f"✗ Error de conexión: {error.reason}"
        )

    except TimeoutError:

        print(
            "✗ La conexión tardó demasiado."
        )

    except Exception as error:

        print(
            f"✗ Error: {error}"
        )

    return None


# ============================================================
#                         NAVEGADOR
# ============================================================

class Browser:

    def __init__(self):

        self.history = []
        self.history_index = -1

        self.current_url = None
        self.current_html = None
        self.current_text = None
        self.current_links = []

    # --------------------------------------------------------
    # OPEN
    # --------------------------------------------------------

    def open(self, url, add_history=True):

        print()
        print(
            f"🌐 Abriendo: {url}"
        )

        result = fetch_page(url)

        if result is None:

            return False

        final_url, content_type, html = result

        if "text/html" not in content_type.lower():

            print(
                f"⚠ Tipo de contenido: {content_type}"
            )

        text = html_to_text(
            html
        )

        links = extract_links(
            html,
            final_url
        )

        self.current_url = final_url
        self.current_html = html
        self.current_text = text
        self.current_links = links

        if add_history:

            if (
                self.history_index >= 0
                and self.history[
                    self.history_index
                ] == final_url
            ):

                pass

            else:

                self.history = self.history[
                    :self.history_index + 1
                ]

                self.history.append(
                    final_url
                )

                self.history_index = (
                    len(self.history) - 1
                )

        print()
        print(
            f"✓ {final_url}"
        )

        print()

        if text:

            print(text)

        else:

            print(
                "(La página no contiene texto visible.)"
            )

        print()

        print(
            f"Enlaces encontrados: {len(links)}"
        )

        return True

    # --------------------------------------------------------
    # LINKS
    # --------------------------------------------------------

    def show_links(self):

        if not self.current_links:

            print(
                "No hay enlaces disponibles."
            )

            return

        print()
        print(
            "Enlaces:"
        )
        print()

        for number, (label, url) in enumerate(
            self.current_links,
            start=1
        ):

            print(
                f"{number}. {label}"
            )

            print(
                f"   {url}"
            )

    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    def back(self):

        if self.history_index <= 0:

            print(
                "No hay una página anterior."
            )

            return

        self.history_index -= 1

        url = self.history[
            self.history_index
        ]

        self.open(
            url,
            add_history=False
        )

    # --------------------------------------------------------
    # FORWARD
    # --------------------------------------------------------

    def forward(self):

        if self.history_index >= (
            len(self.history) - 1
        ):

            print(
                "No hay una página siguiente."
            )

            return

        self.history_index += 1

        url = self.history[
            self.history_index
        ]

        self.open(
            url,
            add_history=False
        )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, filename):

        if not self.current_text:

            print(
                "No hay ninguna página abierta."
            )

            return

        path = Path(
            filename
        ).expanduser()

        if not path.is_absolute():

            path = Path.cwd() / path

        try:

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with path.open(
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    self.current_text
                )

            print(
                f"✓ Página guardada en: {path}"
            )

        except Exception as error:

            print(
                f"✗ Error guardando: {error}"
            )


# ============================================================
#                           ABOUT
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Navegador web de texto de LynaOS.

Funciones:

  • Navegación HTTP/HTTPS
  • Conversión HTML → texto
  • Extracción de enlaces
  • Historial
  • Guardado de páginas
""")


# ============================================================
#                            APP
# ============================================================

def run():

    browser = Browser()

    banner()

    while True:

        try:

            command = input(
                "shelly> "
            ).strip()

        except KeyboardInterrupt:

            print()
            print(
                "Saliendo de Shelly..."
            )

            break

        except EOFError:

            print()

            break

        if not command:
            continue

        parts = command.split(
            None,
            1
        )

        action = parts[0].upper()

        argument = (
            parts[1].strip()
            if len(parts) > 1
            else ""
        )

        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        if action in (
            "Q",
            "EXIT"
        ):

            print(
                "Saliendo de Shelly..."
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
        # OPEN
        # ----------------------------------------------------

        elif action in (
            "OPEN",
            "GO"
        ):

            if not argument:

                print(
                    "Uso: OPEN <URL>"
                )

                continue

            browser.open(
                argument
            )

        # ----------------------------------------------------
        # LINKS
        # ----------------------------------------------------

        elif action == "LINKS":

            browser.show_links()

        # ----------------------------------------------------
        # BACK
        # ----------------------------------------------------

        elif action == "BACK":

            browser.back()

        # ----------------------------------------------------
        # FORWARD
        # ----------------------------------------------------

        elif action == "FORWARD":

            browser.forward()

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        elif action == "SAVE":

            if not argument:

                print(
                    "Uso: SAVE <archivo>"
                )

                continue

            browser.save(
                argument
            )

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        elif action in (
            "CLEAR",
            "CLS"
        ):

            os.system("clear")

        # ----------------------------------------------------
        # ABOUT
        # ----------------------------------------------------

        elif action == "ABOUT":

            about()

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
