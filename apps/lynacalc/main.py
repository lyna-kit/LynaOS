#!/usr/bin/env python3

import ast
import operator
import os


APP_NAME = "LynaCalc"
APP_VERSION = "0.1"

history = []


# ============================================================
#                         CALCULADORA
# ============================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}


def calculate(node):

    if isinstance(node, ast.Expression):
        return calculate(node.body)

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("valor no permitido")

    if isinstance(node, ast.BinOp):

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("operador no permitido")

        left = calculate(node.left)
        right = calculate(node.right)

        if isinstance(
            node.op,
            (ast.Div, ast.Mod, ast.FloorDiv)
        ) and right == 0:
            raise ZeroDivisionError(
                "no se puede dividir entre cero"
            )

        if isinstance(node.op, ast.Pow):

            if abs(right) > 1000:
                raise ValueError(
                    "potencia demasiado grande"
                )

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):

        value = calculate(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return +value

        raise ValueError("operador no permitido")

    raise ValueError("expresión no permitida")


def evaluate(expression):

    expression = expression.strip()

    if not expression:
        raise ValueError("expresión vacía")

    # Porcentaje
    if expression.endswith("%"):

        value = expression[:-1].strip()

        try:
            return float(value) / 100

        except ValueError:
            raise ValueError(
                "porcentaje inválido"
            )

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

    except SyntaxError:

        raise ValueError(
            "expresión inválida"
        )

    result = calculate(tree)

    if isinstance(result, float):

        if result.is_integer():
            return int(result)

    return result


# ============================================================
#                           AYUDA
# ============================================================

def show_help():

    print("""
LynaCalc 0.1

Operaciones:

  2 + 2
  10 - 5
  8 * 4
  20 / 5
  2 ** 8
  10 % 3
  10 // 3
  (20 + 10) / 2
  50%

Comandos:

  help       Mostrar esta ayuda
  history    Mostrar historial
  clear      Limpiar pantalla
  version    Mostrar versión
  about      Información de LynaCalc
  exit       Salir
""")


# ============================================================
#                           ABOUT
# ============================================================

def about():

    print(f"""
{APP_NAME} {APP_VERSION}

Calculadora oficial de LynaOS.

Aplicación: {APP_NAME}
Versión:    {APP_VERSION}
Sistema:    LynaOS
""")


# ============================================================
#                          HISTORIAL
# ============================================================

def show_history():

    if not history:

        print("El historial está vacío.")

        return

    for number, item in enumerate(
        history,
        start=1
    ):

        expression, result = item

        print(
            f"{number}. {expression} = {result}"
        )


# ============================================================
#                         LynaCalc
# ============================================================

def calculator():

    print(f"""
╔══════════════════════════════════╗
║          {APP_NAME} {APP_VERSION}          ║
║       Calculadora LynaOS         ║
╚══════════════════════════════════╝

Escribe 'help' para obtener ayuda.
""")

    while True:

        try:

            expression = input(
                "lynacalc> "
            ).strip()

            if not expression:
                continue

            if expression == "exit":
                break

            if expression == "help":
                show_help()
                continue

            if expression == "history":
                show_history()
                continue

            if expression == "version":

                print(
                    f"{APP_NAME} {APP_VERSION}"
                )

                continue

            if expression == "about":

                about()

                continue

            if expression == "clear":

                os.system("clear")

                continue

            try:

                result = evaluate(
                    expression
                )

                print(result)

                history.append(
                    (
                        expression,
                        result
                    )
                )

            except ZeroDivisionError as error:

                print(
                    f"Error: {error}"
                )

            except ValueError as error:

                print(
                    f"Error: {error}"
                )

            except OverflowError:

                print(
                    "Error: resultado demasiado grande."
                )

        except KeyboardInterrupt:

            print()
            break

        except EOFError:

            print()
            break


# ============================================================
#                           MAIN
# ============================================================

if __name__ == "__main__":
    calculator()
