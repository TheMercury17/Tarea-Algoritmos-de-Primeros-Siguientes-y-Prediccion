"""
Pruebas unitarias para validar que los algoritmos de PRIMEROS, SIGUIENTES y PREDICCIÓN
coinciden exactamente al 100% con los resultados analíticos calculados formalmente.

Autores: Grupo 5
- Andrés Sebastián Coral Vallejo
- Carol Arenas Cardona
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import unittest
from ejercicio1 import construir_gramatica_1, SOLUCION_ANALITICA_1
from ejercicio2 import construir_gramatica_2, SOLUCION_ANALITICA_2


class TestAlgoritmosGramaticas(unittest.TestCase):

    def test_ejercicio_1_primeros(self):
        g = construir_gramatica_1()
        primeros = g.calcular_primeros()
        for nt, esperado in SOLUCION_ANALITICA_1["PRIMEROS"].items():
            self.assertEqual(primeros[nt], esperado, f"Fallo en PRIMEROS({nt}) Ejercicio 1")

    def test_ejercicio_1_siguientes(self):
        g = construir_gramatica_1()
        primeros = g.calcular_primeros()
        siguientes = g.calcular_siguientes(primeros)
        for nt, esperado in SOLUCION_ANALITICA_1["SIGUIENTES"].items():
            self.assertEqual(siguientes[nt], esperado, f"Fallo en SIGUIENTES({nt}) Ejercicio 1")

    def test_ejercicio_1_prediccion(self):
        g = construir_gramatica_1()
        primeros = g.calcular_primeros()
        siguientes = g.calcular_siguientes(primeros)
        predicciones = g.calcular_prediccion(primeros, siguientes)
        for id_regla, esperado in SOLUCION_ANALITICA_1["PREDICCION"].items():
            regla, pred = predicciones[id_regla]
            self.assertEqual(pred, esperado, f"Fallo en PRED({regla}) Ejercicio 1")

    def test_ejercicio_2_primeros(self):
        g = construir_gramatica_2()
        primeros = g.calcular_primeros()
        for nt, esperado in SOLUCION_ANALITICA_2["PRIMEROS"].items():
            self.assertEqual(primeros[nt], esperado, f"Fallo en PRIMEROS({nt}) Ejercicio 2")

    def test_ejercicio_2_siguientes(self):
        g = construir_gramatica_2()
        primeros = g.calcular_primeros()
        siguientes = g.calcular_siguientes(primeros)
        for nt, esperado in SOLUCION_ANALITICA_2["SIGUIENTES"].items():
            self.assertEqual(siguientes[nt], esperado, f"Fallo en SIGUIENTES({nt}) Ejercicio 2")

    def test_ejercicio_2_prediccion(self):
        g = construir_gramatica_2()
        primeros = g.calcular_primeros()
        siguientes = g.calcular_siguientes(primeros)
        predicciones = g.calcular_prediccion(primeros, siguientes)
        for id_regla, esperado in SOLUCION_ANALITICA_2["PREDICCION"].items():
            regla, pred = predicciones[id_regla]
            self.assertEqual(pred, esperado, f"Fallo en PRED({regla}) Ejercicio 2")


if __name__ == "__main__":
    unittest.main()
