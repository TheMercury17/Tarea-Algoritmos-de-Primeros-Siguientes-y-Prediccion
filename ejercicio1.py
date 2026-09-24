"""
Ejercicio 1: Gramática 1
Cálculo de Primeros, Siguientes y Predicción.

Gramática:
S -> A uno B C
S -> S dos
A -> B C D
A -> A tres
A -> ε
B -> D cuatro C tres
B -> ε
C -> cinco D B
C -> ε
D -> seis
D -> ε
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from gramatica import Gramatica, EPSILON, FIN_CADENA


def construir_gramatica_1() -> Gramatica:
    no_terminales = ['S', 'A', 'B', 'C', 'D']
    terminales = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis']
    g = Gramatica(no_terminales=no_terminales, terminales=terminales, inicial='S')

    # Reglas
    g.agregar_regla('S', ['A', 'uno', 'B', 'C'])       # Regla 1
    g.agregar_regla('S', ['S', 'dos'])                 # Regla 2
    g.agregar_regla('A', ['B', 'C', 'D'])              # Regla 3
    g.agregar_regla('A', ['A', 'tres'])                # Regla 4
    g.agregar_regla('A', [EPSILON])                    # Regla 5
    g.agregar_regla('B', ['D', 'cuatro', 'C', 'tres'])  # Regla 6
    g.agregar_regla('B', [EPSILON])                    # Regla 7
    g.agregar_regla('C', ['cinco', 'D', 'B'])          # Regla 8
    g.agregar_regla('C', [EPSILON])                    # Regla 9
    g.agregar_regla('D', ['seis'])                     # Regla 10
    g.agregar_regla('D', [EPSILON])                    # Regla 11

    return g


# Solución analítica esperada para comparar
SOLUCION_ANALITICA_1 = {
    "PRIMEROS": {
        "S": {"uno", "cuatro", "cinco", "seis", "tres"},
        "A": {"cuatro", "cinco", "seis", "tres", EPSILON},
        "B": {"cuatro", "seis", EPSILON},
        "C": {"cinco", EPSILON},
        "D": {"seis", EPSILON}
    },
    "SIGUIENTES": {
        "S": {FIN_CADENA, "dos"},
        "A": {"uno", "tres"},
        "B": {FIN_CADENA, "dos", "uno", "tres", "cinco", "seis"},
        "C": {FIN_CADENA, "dos", "uno", "tres", "seis"},
        "D": {FIN_CADENA, "dos", "uno", "tres", "cuatro", "seis"}
    },
    "PREDICCION": {
        1: {"uno", "cuatro", "cinco", "seis", "tres"},
        2: {"uno", "cuatro", "cinco", "seis", "tres"},
        3: {"uno", "tres", "cuatro", "cinco", "seis"},
        4: {"tres", "cuatro", "cinco", "seis"},
        5: {"uno", "tres"},
        6: {"cuatro", "seis"},
        7: {FIN_CADENA, "dos", "uno", "tres", "cinco", "seis"},
        8: {"cinco"},
        9: {FIN_CADENA, "dos", "uno", "tres", "seis"},
        10: {"seis"},
        11: {FIN_CADENA, "dos", "uno", "tres", "cuatro", "seis"}
    }
}


def ejecutar_ejercicio_1():
    g = construir_gramatica_1()
    print("=" * 70)
    print("EJERCICIO 1: GRAMÁTICA 1")
    print("=" * 70)
    print("\nReglas de la gramática:")
    for r in g.reglas:
        print(f"  {r}")

    primeros = g.calcular_primeros()
    siguientes = g.calcular_siguientes(primeros)
    predicciones = g.calcular_prediccion(primeros, siguientes)
    es_ll1, conflictos = g.verificar_ll1(predicciones)

    print("\n--- CONJUNTOS DE PRIMEROS ---")
    for nt in g.no_terminales:
        elems = ", ".join(sorted(primeros[nt]))
        print(f"  PRIMEROS({nt}) = {{ {elems} }}")

    print("\n--- CONJUNTOS DE SIGUIENTES ---")
    for nt in g.no_terminales:
        elems = ", ".join(sorted(siguientes[nt]))
        print(f"  SIGUIENTES({nt}) = {{ {elems} }}")

    print("\n--- CONJUNTOS DE PREDICCIÓN ---")
    for id_regla, (regla, pred) in predicciones.items():
        elems = ", ".join(sorted(pred))
        print(f"  PRED({regla}) = {{ {elems} }}")

    print("\n--- EVALUACIÓN LL(1) ---")
    if es_ll1:
        print("  La gramática ES LL(1).")
    else:
        print("  La gramática NO es LL(1). Conflictos detectados:")
        for c in conflictos:
            print(f"   - {c}")

    return g, primeros, siguientes, predicciones


if __name__ == "__main__":
    ejecutar_ejercicio_1()
