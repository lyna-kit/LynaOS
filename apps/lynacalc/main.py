#!/usr/bin/env python3

import ast
import math
import operator


APP_NAME = "LynaCalc"
APP_VERSION = "0.3"


# ============================================================
#                         OPERADORES
# ============================================================

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


# ============================================================
#                         FUNCIONES
# ============================================================

FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


# ============================================================
#                      EVALUADOR SEGURO
# ============================================================

def evaluate_node(node):

    if isinstance(node, ast.Expression):

        return evaluate_node(node.body)

    # --------------------------------------------------------
    # Números
    # --------------------------------------------------------

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):

            return node.value

        raise ValueError(
            "Valor no permitido."
        )

    # --------------------------------------------------------
    # Operaciones binarias
    # --------------------------------------------------------

    if isinstance(node, ast.BinOp):

        operation = BINARY_OPERATORS.get(
            type(node.op)
        )

        if operation is None:

            raise ValueError(
                "Operador no permitido."
            )

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        # Evitar potencias absurdamente grandes.

        if isinstance(node.op, ast.Pow):

            if abs(right) > 1000:

                raise ValueError(
                    "Exponente demasiado grande."
                )

        return operation(left, right)

    # --------------------------------------------------------
    # Operaciones unarias
    # --------------------------------------------------------

    if isinstance(node, ast.UnaryOp):

        operation = UNARY_OPERATORS.get(
            type(node.op)
        )

        if operation is None:

            raise ValueError(
                "Operador no permitido."
            )

        return operation(
            evaluate_node(node.operand)
        )

    # --------------------------------------------------------
    # Variables / constantes
    # --------------------------------------------------------

    if isinstance(node, ast.Name):

        if node.id in CONSTANTS:

            return CONSTANTS[node.id]

        raise ValueError(
            f"Nombre no permitido: {node.id}"
        )

    # --------------------------------------------------------
    # Funciones
    # --------------------------------------------------------

    if isinstance(node, ast.Call):

        if not isinstance(
            node.func,
            ast.Name
        ):

            raise ValueError(
                "Función no permitida."
            )

        name = node.func.id

        if name not in FUNCTIONS:

            raise ValueError(
                f"Función desconocida: {name}"
            )

        if node.keywords:

            raise ValueError(
                "Argumentos con nombre no permitidos."
            )

        arguments = [
            evaluate_node(argument)
            for argument in node.args
        ]

        return FUNCTIONS[name](
            *arguments
        )

    raise ValueError(
        "Expresión no permitida."
    )


def calculate(expression):

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        return evaluate_node(tree)

    except ZeroDivisionError:

        raise ValueError(
            "No se puede dividir entre cero."
        )

    except OverflowError:

        raise ValueError(
            "Resultado demasiado grande."
        )

    except SyntaxError:

        raise ValueError(
            "Expresión inválida."
        )


# ============================================================
#                         FORMATO
# ============================================================

def format_result(result):

    if isinstance(result, float):

        if result.is_integer():

            return str(int(result))

        return f"{result:.12g}"

    return str(result)


# ============================================================
#                         BANNER
# ============================================================

def banner():

    print("""
╔══════════════════════════════════════╗
║          LynaCalc 0.3                ║
║       Calculadora de LynaOS         ║
╚══════════════════════════════════════╝

Operadores:
  +   Suma
  -   Resta
  *   Multiplicación
  /   División
  //  División entera
  %   Módulo
  **  Potencia

Funciones:
  sqrt(x)
  abs(x)
  round(x)
  floor(x)
  ceil(x)

Constantes:
  pi
  e

Comandos:
  history    Ver historial
  clear      Limpiar historial
  help       Mostrar ayuda
  exit       Salir

Ejemplo:
  (10 + 5) * 2
""")


# ============================================================
#                          AYUDA
# ============================================================

def help_command():

    print("""
LynaCalc 0.3

Puedes introducir directamente una operación:

  10 + 5
  20 / 4
  2 ** 8
  10 % 3
  (5 + 3) * 2

Funciones:

  sqrt(25)
  abs(-10)
  round(3.14159, 2)
  floor(3.9)
  ceil(3.1)

Constantes:

  pi
  e

Comandos:

  history
  clear
  help
  exit
""")


# ============================================================
#                         HISTORIAL
# ============================================================

def show_history(history):

    if not history:

        print(
            "El historial está vacío."
        )

        return

    print()
    print("Historial:")
    print()

    for number, entry in enumerate(
        history,
        start=1
    ):

        print(
            f"  {number}. {entry}"
        )


def clear_history(history):

    history.clear()

    print(
        "✓ Historial limpiado."
    )


# ============================================================
#                            APP
# ============================================================

def run():

    history = []

    banner()

    while True:

        try:

            expression = input(
                "lynacalc> "
            ).strip()

        except KeyboardInterrupt:

            print()
            print(
                "Saliendo de LynaCalc..."
            )

            break

        except EOFError:

            print()

            break

        if not expression:

            continue

        command = expression.lower()

        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        if command in (
            "exit",
            "quit",
            "q"
        ):

            print(
                "Saliendo de LynaCalc..."
            )

            break

        # ----------------------------------------------------
        # AYUDA
        # ----------------------------------------------------

        if command in (
            "help",
            "h"
        ):

            help_command()

            continue

        # ----------------------------------------------------
        # HISTORIAL
        # ----------------------------------------------------

        if command in (
            "history",
            "hist"
        ):

            show_history(history)

            continue

        # ----------------------------------------------------
        # LIMPIAR
        # ----------------------------------------------------

        if command in (
            "clear",
            "cls"
        ):

            clear_history(history)

            continue

        # ----------------------------------------------------
        # CALCULAR
        # ----------------------------------------------------

        try:

            result = calculate(
                expression
            )

            formatted = format_result(
                result
            )

            print(
                f"= {formatted}"
            )

            history.append(
                f"{expression} = {formatted}"
            )

        except ValueError as error:

            print(
                f"✗ Error: {error}"
            )

        except Exception as error:

            print(
                f"✗ Error inesperado: {error}"
            )


# ============================================================
#                            MAIN
# ============================================================

if __name__ == "__main__":
    run()
