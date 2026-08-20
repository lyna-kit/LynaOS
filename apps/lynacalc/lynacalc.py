#!/usr/bin/env python3

import ast
import math
import operator


APP_NAME = "LynaCalc"
APP_VERSION = "0.4"


# ============================================================
# OPERADORES PERMITIDOS
# ============================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


# ============================================================
# EVALUADOR SEGURO
# ============================================================

def calculate(expression):
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("^", "**")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate_node(tree.body)

    except ZeroDivisionError:
        raise ValueError("No se puede dividir entre cero.")

    except (SyntaxError, ValueError, TypeError, OverflowError):
        raise ValueError("Operación no válida.")


def evaluate_node(node):

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Valor no permitido.")

    if isinstance(node, ast.BinOp):
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Operador no permitido.")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        # Evitar potencias absurdamente grandes
        if isinstance(node.op, ast.Pow):
            if abs(right) > 1000:
                raise ValueError("Exponente demasiado grande.")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Operador no permitido.")

        return operation(evaluate_node(node.operand))

    raise ValueError("Expresión no permitida.")


# ============================================================
# RAÍZ CUADRADA
# ============================================================

def square_root(value):

    try:
        value = float(value)

        if value < 0:
            print("\nError: no existe raíz real de un número negativo.")
            return

        result = math.sqrt(value)
        print_result(result)

    except ValueError:
        print("\nError: número no válido.")


# ============================================================
# FORMATO DE RESULTADOS
# ============================================================

def format_number(number):

    if isinstance(number, float):

        if math.isfinite(number):

            if number.is_integer():
                return str(int(number))

            return f"{number:.12g}"

    return str(number)


def print_result(result):

    if isinstance(result, complex):
        print(f"\nResultado: {result}")
        return

    print(f"\nResultado: {format_number(result)}")


# ============================================================
# HISTORIAL
# ============================================================

history = []


def show_history():

    print("\n" + "=" * 50)
    print(" HISTORIAL")
    print("=" * 50)

    if not history:
        print("No hay operaciones todavía.")
    else:
        for number, (expression, result) in enumerate(history, 1):
            print(
                f"{number}. {expression} = "
                f"{format_number(result)}"
            )

    print("=" * 50)


def clear_history():

    history.clear()
    print("\nHistorial eliminado.")


# ============================================================
# AYUDA
# ============================================================

def show_help():

    print("""
==================================================
                 LynaCalc 0.4
==================================================

Operaciones:

  2 + 2          Suma
  5 - 3          Resta
  4 * 6          Multiplicación
  20 / 5         División
  10 % 3         Módulo
  2 ** 8         Potencia
  2 ^ 8          Potencia

Operaciones combinadas:

  (10 + 5) * 2
  100 / (5 + 5)
  2 ** 3 + 10

Raíz cuadrada:

  sqrt 25

Comandos:

  help       Mostrar ayuda
  history    Mostrar historial
  clear      Borrar historial
  version    Mostrar versión
  q          Salir
  exit       Salir

==================================================
""")


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

def main():

    print("=" * 50)
    print("              LynaCalc 0.4")
    print("          Calculadora de LynaOS")
    print("=" * 50)
    print("Escribe 'help' para ver los comandos.")
    print()

    while True:

        try:
            expression = input("LynaCalc> ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo de LynaCalc...")
            break

        if not expression:
            continue

        command = expression.lower()

        # ----------------------------
        # SALIR
        # ----------------------------

        if command in ("q", "quit", "exit"):

            print("Saliendo de LynaCalc...")
            break

        # ----------------------------
        # AYUDA
        # ----------------------------

        if command in ("help", "?"):

            show_help()
            continue

        # ----------------------------
        # HISTORIAL
        # ----------------------------

        if command == "history":

            show_history()
            continue

        # ----------------------------
        # LIMPIAR HISTORIAL
        # ----------------------------

        if command == "clear":

            clear_history()
            continue

        # ----------------------------
        # VERSIÓN
        # ----------------------------

        if command == "version":

            print(f"\n{APP_NAME} {APP_VERSION}")
            continue

        # ----------------------------
        # RAÍZ CUADRADA
        # ----------------------------

        if command.startswith("sqrt"):

            value = expression[4:].strip()

            if not value:
                print("\nUso: sqrt <número>")
                continue

            try:
                result = calculate(value)

                if result < 0:
                    print(
                        "\nError: no existe raíz real "
                        "de un número negativo."
                    )
                    continue

                result = math.sqrt(result)

                print_result(result)

                history.append(
                    (f"sqrt({value})", result)
                )

            except ValueError as error:
                print(f"\nError: {error}")

            continue

        # ----------------------------
        # CÁLCULO NORMAL
        # ----------------------------

        try:

            result = calculate(expression)

            print_result(result)

            history.append(
                (expression, result)
            )

        except ValueError as error:

            print(f"\nError: {error}")


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()
