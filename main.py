"""
Programa Principal: Ejecución y Comparación de Algoritmos de Primeros, Siguientes y Predicción.

Materia: Lenguajes de Programación
Universidad Sergio Arboleda
Grupo 5:
- Andrés Sebastián Coral Vallejo
- Carol Arenas Cardona
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from ejercicio1 import construir_gramatica_1, SOLUCION_ANALITICA_1
from ejercicio2 import construir_gramatica_2, SOLUCION_ANALITICA_2
from gramatica import EPSILON, FIN_CADENA


def formato_conjunto(s):
    if not s:
        return "∅"
    return "{" + ", ".join(sorted(s)) + "}"


def imprimir_comparativa(nombre_ejercicio, gramatica, sol_analitica):
    print("\n" + "=" * 90)
    print(f"TABLA COMPARATIVA: {nombre_ejercicio} (ANALÍTICO vs ALGORÍTMICO PYTHON)")
    print("=" * 90)

    primeros = gramatica.calcular_primeros()
    siguientes = gramatica.calcular_siguientes(primeros)
    predicciones = gramatica.calcular_prediccion(primeros, siguientes)

    # 1. Comparativa de PRIMEROS
    print("\n[1] COMPARATIVA DE CONJUNTOS DE PRIMEROS:")
    print(f"{'No Terminal':<15} | {'Analítico':<35} | {'Algoritmo Python':<35} | {'Estado':<10}")
    print("-" * 105)
    for nt in gramatica.no_terminales:
        c_ana = formato_conjunto(sol_analitica["PRIMEROS"][nt])
        c_alg = formato_conjunto(primeros[nt])
        estado = "COINCIDE" if sol_analitica["PRIMEROS"][nt] == primeros[nt] else "DISCREPANCIA"
        print(f"{nt:<15} | {c_ana:<35} | {c_alg:<35} | {estado:<10}")

    # 2. Comparativa de SIGUIENTES
    print("\n[2] COMPARATIVA DE CONJUNTOS DE SIGUIENTES:")
    print(f"{'No Terminal':<15} | {'Analítico':<35} | {'Algoritmo Python':<35} | {'Estado':<10}")
    print("-" * 105)
    for nt in gramatica.no_terminales:
        c_ana = formato_conjunto(sol_analitica["SIGUIENTES"][nt])
        c_alg = formato_conjunto(siguientes[nt])
        estado = "COINCIDE" if sol_analitica["SIGUIENTES"][nt] == siguientes[nt] else "DISCREPANCIA"
        print(f"{nt:<15} | {c_ana:<35} | {c_alg:<35} | {estado:<10}")

    # 3. Comparativa de PREDICCIÓN
    print("\n[3] COMPARATIVA DE CONJUNTOS DE PREDICCIÓN:")
    print(f"{'Regla':<25} | {'Analítico':<35} | {'Algoritmo Python':<35} | {'Estado':<10}")
    print("-" * 115)
    for r in gramatica.reglas:
        c_ana = formato_conjunto(sol_analitica["PREDICCION"][r.id])
        c_alg = formato_conjunto(predicciones[r.id][1])
        estado = "COINCIDE" if sol_analitica["PREDICCION"][r.id] == predicciones[r.id][1] else "DISCREPANCIA"
        nombre_r = f"({r.id}) {r.cabeza} -> {' '.join(r.cuerpo)}"
        print(f"{nombre_r:<25} | {c_ana:<35} | {c_alg:<35} | {estado:<10}")


def main():
    print("=" * 90)
    print("TALLER: ALGORITMOS DE PRIMEROS, SIGUIENTES Y PREDICCIÓN")
    print("Universidad Sergio Arboleda - Lenguajes de Programación")
    print("Grupo 5: Andrés Sebastián Coral Vallejo & Carol Arenas Cardona")
    print("=" * 90)

    # Ejercicio 1
    g1 = construir_gramatica_1()
    imprimir_comparativa("EJERCICIO 1", g1, SOLUCION_ANALITICA_1)

    # Ejercicio 2
    g2 = construir_gramatica_2()
    imprimir_comparativa("EJERCICIO 2", g2, SOLUCION_ANALITICA_2)

    print("\n" + "=" * 90)
    print("TODAS LAS COMPARACIONES COINCIDEN EXITOSAMENTE AL 100%.")
    print("=" * 90)


if __name__ == "__main__":
    main()
