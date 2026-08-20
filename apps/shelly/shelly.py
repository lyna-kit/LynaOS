#!/usr/bin/env python3

import os
import re
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse


APP_NAME = "Shelly"
APP_VERSION = "0.4"

USER_AGENT = "Shelly/0.4 LynaOS"

MAX_DOWNLOAD_SIZE = 5 * 1024 * 1024


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════════════════════════╗
║                       Shelly 0.4                         ║
║                  Navegador de texto                     ║
╚══════════════════════════════════════════════════════════╝

Escribe H para ver la ayuda.
Escribe Q para salir.
""")


# ============================================================
#                           AYUDA
# ============================================================

def help_command():

    print("""
Shelly 0.4

NAVEGACIÓN

  OPEN <URL>       Abrir una página web
  OPEN <número>    Abrir un enlace de LINKS
  GO <URL>         Alias de OPEN
  BACK             Página anterior
  FORWARD          Página siguiente
  RELOAD           Recargar la página actual
  HOME             Volver a la página inicial
  HISTORY          Mostrar historial

ENLACES

  LINKS            Mostrar enlaces encontrados

ARCHIVOS

  SAVE <archivo>   Guardar el texto de la página

SISTEMA

  CLEAR            Limpiar pantalla
  ABOUT            Información
  H                Ayuda
  Q                Salir

EJEMPLOS

  OPEN https://example.com
  LINKS
  OPEN 2
  BACK
  FORWARD
  RELOAD
  HISTORY
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

    # Eliminar contenido no visible.

    html = re.sub(
        r"<noscript\b[^>]*>.*?</noscript>",
        " ",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Separadores.

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
        r"</li\s*>",
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
        r"\n[ \t]+",
        "\n",
        text
    )

    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text
    )

    text = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
#                         TÍTULO
# ============================================================

def extract_title(html):

    match = re.search(
        r"<title\b[^>]*>(.*?)</title>",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return ""

    title = html_to_text(
        match.group(1)
    )

    return title.strip()


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

    parsed = urlparse(url)

    if parsed.scheme not in (
        "http",
        "https"
    ):
        print("✗ URL no válida.")
        return None

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
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

            content_length = response.headers.get(
                "Content-Length"
            )

            if content_length:

                try:

                    if int(content_length) > MAX_DOWNLOAD_SIZE:

                        print(
                            "✗ La página es demasiado grande."
                        )

                        return None

                except ValueError:
                    pass

            data = response.read(
                MAX_DOWNLOAD_SIZE + 1
            )

            if len(data) > MAX_DOWNLOAD_SIZE:

                print(
                    "✗ La página supera el límite de 5 MB."
                )

                return None

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
        self.current_title = None
        self.current_links = []

        self.home_url = None

    # --------------------------------------------------------
    # OPEN
    # --------------------------------------------------------

    def open(self, url, add_history=True):

        # Abrir enlace mediante número.

        if (
            url.isdigit()
            and self.current_links
        ):

            number = int(url)

            if number < 1 or number > len(
                self.current_links
            ):

                print(
                    "✗ Número de enlace no válido."
                )

                return False

            url = self.current_links[
                number - 1
            ][1]

        print()
        print(
            f"🌐 Abriendo: {url}"
        )

        result = fetch_page(url)

        if result is None:
            return False

        final_url, content_type, html = result

        if (
            "text/html" not in
            content_type.lower()
        ):

            print(
                f"⚠ Tipo de contenido: {content_type}"
            )

        text = html_to_text(
            html
        )

        title = extract_title(
            html
        )

        links = extract_links(
            html,
            final_url
        )

        self.current_url = final_url
        self.current_html = html
        self.current_text = text
        self.current_title = title
        self.current_links = links

        if self.home_url is None:
            self.home_url = final_url

        if add_history:

            self.history = self.history[
                :self.history_index + 1
            ]

            if (
                not self.history
                or self.history[-1] != final_url
            ):

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

        if title:

            print(
                f"📄 {title}"
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
        print("Enlaces:")
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

        print()

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
    # RELOAD
    # --------------------------------------------------------

    def reload(self):

        if not self.current_url:

            print(
                "No hay ninguna página abierta."
            )

            return

        self.open(
            self.current_url,
            add_history=False
        )

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    def home(self):

        if not self.home_url:

            print(
                "No hay página inicial."
            )

            return

        self.open(
            self.home_url
        )

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    def show_history(self):

        if not self.history:

            print(
                "El historial está vacío."
            )

            return

        print()
        print("Historial:")
        print()

        for number, url in enumerate(
            self.history,
            start=1
        ):

            marker = ""

            if (
                number - 1
                == self.history_index
            ):

                marker = " ← actual"

            print(
                f"{number}. {url}{marker}"
            )

        print()

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

        except OSError as error:

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
  • Apertura de enlaces por número
  • Historial de navegación
  • BACK / FORWARD
  • RELOAD / HOME
  • Guardado de páginas
  • Límite de descarga de 5 MB
""")


# ============================================================
#                            APP
# ============================================================

def run():

    browser = Browser()

    banner()

    while True:

        try:

            prompt = "shelly"

            if browser.current_url:

                hostname = urlparse(
                    browser.current_url
                ).netloc

                if hostname:
                    prompt = f"shelly:{hostname}"

            command = input(
                f"{prompt}> "
            ).strip()

        except KeyboardInterrupt:

            print()
            print(
                "Saliendo de Shelly..."
            )

            break

        except EOFError:

            print()
            print(
                "Saliendo de Shelly..."
            )

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
            "EXIT",
            "QUIT"
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
        # RELOAD
        # ----------------------------------------------------

        elif action == "RELOAD":

            browser.reload()

        # ----------------------------------------------------
        # HOME
        # ----------------------------------------------------

        elif action == "HOME":

            browser.home()

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        elif action == "HISTORY":

            browser.show_history()

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
