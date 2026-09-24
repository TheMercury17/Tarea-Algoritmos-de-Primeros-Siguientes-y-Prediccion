"""
Ejercicio 2: Gramática 2
Cálculo de Primeros, Siguientes y Predicción.

Gramática:
S -> A B uno
A -> dos B
A -> ε
B -> C D
B -> tres
B -> ε
C -> cuatro A B
C -> cinco
D -> seis
D -> ε
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from gramatica import Gramatica, EPSILON, FIN_CADENA


def construir_gramatica_2() -> Gramatica:
    no_terminales = ['S', 'A', 'B', 'C', 'D']
    terminales = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis']
    g = Gramatica(no_terminales=no_terminales, terminales=terminales, inicial='S')

    # Reglas
    g.agregar_regla('S', ['A', 'B', 'uno'])       # Regla 1
    g.agregar_regla('A', ['dos', 'B'])           # Regla 2
    g.agregar_regla('A', [EPSILON])              # Regla 3
    g.agregar_regla('B', ['C', 'D'])             # Regla 4
    g.agregar_regla('B', ['tres'])               # Regla 5
    g.agregar_regla('B', [EPSILON])              # Regla 6
    g.agregar_regla('C', ['cuatro', 'A', 'B'])   # Regla 7
    g.agregar_regla('C', ['cinco'])              # Regla 8
    g.agregar_regla('D', ['seis'])               # Regla 9
    g.agregar_regla('D', [EPSILON])              # Regla 10

    return g


# Solución analítica esperada para comparar
SOLUCION_ANALITICA_2 = {
    "PRIMEROS": {
        "S": {"uno", "dos", "tres", "cuatro", "cinco"},
        "A": {"dos", EPSILON},
        "B": {"tres", "cuatro", "cinco", EPSILON},
        "C": {"cuatro", "cinco"},
        "D": {"seis", EPSILON}
    },
    "SIGUIENTES": {
        "S": {FIN_CADENA},
        "A": {"uno", "tres", "cuatro", "cinco", "seis"},
        "B": {"uno", "tres", "cuatro", "cinco", "seis"},
        "C": {"uno", "tres", "cuatro", "cinco", "seis"},
        "D": {"uno", "tres", "cuatro", "cinco", "seis"}
    },
    "PREDICCION": {
        1: {"uno", "dos", "tres", "cuatro", "cinco"},
        2: {"dos"},
        3: {"uno", "tres", "cuatro", "cinco", "seis"},
        4: {"cuatro", "cinco"},
        5: {"tres"},
        6: {"uno", "tres", "cuatro", "cinco", "seis"},
        7: {"cuatro"},
        8: {"cinco"},
        9: {"seis"},
        10: {"uno", "tres", "cuatro", "cinco", "seis"}
    }
}


def ejecutar_ejercicio_2():
    g = construir_gramatica_2()
    print("=" * 70)
    print("EJERCICIO 2: GRAMÁTICA 2")
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
    ejecutar_ejercicio_2()
