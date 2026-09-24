"""
Módulo para el modelado de Gramáticas Libres de Contexto (GLC)
y el cálculo de los conjuntos de PRIMEROS, SIGUIENTES y PREDICCIÓN.

Autores: Grupo 5
- Andrés Sebastián Coral Vallejo
- Carol Arenas Cardona
Materia: Lenguajes de Programación
Universidad Sergio Arboleda
"""

import sys

# Asegurar codificación UTF-8 en consola para caracteres como ε
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from typing import List, Dict, Set, Tuple

EPSILON = 'ε'
FIN_CADENA = '$'


class Regla:
    def __init__(self, id_regla: int, cabeza: str, cuerpo: List[str]):
        self.id = id_regla
        self.cabeza = cabeza
        self.cuerpo = list(cuerpo)

    def es_epsilon(self) -> bool:
        return self.cuerpo == [EPSILON] or len(self.cuerpo) == 0

    def __repr__(self):
        cuerpo_str = " ".join(self.cuerpo) if self.cuerpo else EPSILON
        return f"({self.id}) {self.cabeza} -> {cuerpo_str}"


class Gramatica:
    def __init__(self, no_terminales: List[str], terminales: List[str], inicial: str):
        self.no_terminales: List[str] = no_terminales
        self.terminales: List[str] = terminales
        self.inicial: str = inicial
        self.reglas: List[Regla] = []
        self._contador_reglas = 1

    def agregar_regla(self, cabeza: str, cuerpo: List[str]):
        if not cuerpo:
            cuerpo = [EPSILON]
        regla = Regla(self._contador_reglas, cabeza, cuerpo)
        self.reglas.append(regla)
        self._contador_reglas += 1
        return regla

    def es_terminal(self, simbolo: str) -> bool:
        return simbolo in self.terminales or simbolo == FIN_CADENA

    def es_no_terminal(self, simbolo: str) -> bool:
        return simbolo in self.no_terminales

    def calcular_primeros(self) -> Dict[str, Set[str]]:
        """
        Calcula el conjunto PRIMEROS para todos los símbolos (terminales y no terminales)
        utilizando el algoritmo de punto fijo (iterativo).
        """
        primeros: Dict[str, Set[str]] = {nt: set() for nt in self.no_terminales}
        for t in self.terminales:
            primeros[t] = {t}
        primeros[EPSILON] = {EPSILON}
        primeros[FIN_CADENA] = {FIN_CADENA}

        cambio = True
        while cambio:
            cambio = False
            for regla in self.reglas:
                A = regla.cabeza
                cuerpo = regla.cuerpo

                if regla.es_epsilon():
                    if EPSILON not in primeros[A]:
                        primeros[A].add(EPSILON)
                        cambio = True
                    continue

                # Para A -> Y1 Y2 ... Yk
                todos_derivan_epsilon = True
                for Y in cuerpo:
                    # Añadir PRIMEROS(Y) - {ε}
                    primeros_Y = primeros.get(Y, {Y})
                    elementos_a_anadir = primeros_Y - {EPSILON}
                    if not elementos_a_anadir.issubset(primeros[A]):
                        primeros[A].update(elementos_a_anadir)
                        cambio = True

                    if EPSILON not in primeros_Y:
                        todos_derivan_epsilon = False
                        break

                if todos_derivan_epsilon:
                    if EPSILON not in primeros[A]:
                        primeros[A].add(EPSILON)
                        cambio = True

        return {nt: primeros[nt] for nt in self.no_terminales}

    def calcular_primeros_cadena(self, cadena: List[str], primeros_simbolos: Dict[str, Set[str]]) -> Set[str]:
        """
        Calcula el conjunto PRIMEROS de una secuencia de símbolos α = X1 X2 ... Xk.
        """
        if not cadena or cadena == [EPSILON]:
            return {EPSILON}

        resultado: Set[str] = set()
        todos_derivan_epsilon = True

        for simbolo in cadena:
            if self.es_terminal(simbolo):
                resultado.add(simbolo)
                todos_derivan_epsilon = False
                break
            elif simbolo == EPSILON:
                continue
            else:
                primeros_X = primeros_simbolos.get(simbolo, set())
                resultado.update(primeros_X - {EPSILON})
                if EPSILON not in primeros_X:
                    todos_derivan_epsilon = False
                    break

        if todos_derivan_epsilon:
            resultado.add(EPSILON)

        return resultado

    def calcular_siguientes(self, primeros_simbolos: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
        """
        Calcula el conjunto SIGUIENTES para todos los no terminales
        utilizando el algoritmo de punto fijo.
        """
        siguientes: Dict[str, Set[str]] = {nt: set() for nt in self.no_terminales}
        siguientes[self.inicial].add(FIN_CADENA)

        cambio = True
        while cambio:
            cambio = False
            for regla in self.reglas:
                A = regla.cabeza
                cuerpo = regla.cuerpo

                if regla.es_epsilon():
                    continue

                for i, B in enumerate(cuerpo):
                    if not self.es_no_terminal(B):
                        continue

                    beta = cuerpo[i + 1:]
                    if beta:
                        primeros_beta = self.calcular_primeros_cadena(beta, primeros_simbolos)
                        # Regla: FIRST(β) - {ε} entra en FOLLOW(B)
                        elementos = primeros_beta - {EPSILON}
                        if not elementos.issubset(siguientes[B]):
                            siguientes[B].update(elementos)
                            cambio = True

                        # Regla: Si ε ∈ FIRST(β), FOLLOW(A) entra en FOLLOW(B)
                        if EPSILON in primeros_beta:
                            if not siguientes[A].issubset(siguientes[B]):
                                siguientes[B].update(siguientes[A])
                                cambio = True
                    else:
                        # Regla: A -> α B => FOLLOW(A) entra en FOLLOW(B)
                        if not siguientes[A].issubset(siguientes[B]):
                            siguientes[B].update(siguientes[A])
                            cambio = True

        return siguientes

    def calcular_prediccion(self, primeros_simbolos: Dict[str, Set[str]],
                            siguientes: Dict[str, Set[str]]) -> Dict[int, Tuple[Regla, Set[str]]]:
        """
        Calcula el conjunto de PREDICCIÓN para cada regla A -> α:
        - Si ε ∉ PRIMEROS(α): PRED(A -> α) = PRIMEROS(α)
        - Si ε ∈ PRIMEROS(α): PRED(A -> α) = (PRIMEROS(α) - {ε}) ∪ SIGUIENTES(A)
        """
        predicciones: Dict[int, Tuple[Regla, Set[str]]] = {}

        for regla in self.reglas:
            A = regla.cabeza
            alpha = regla.cuerpo

            if regla.es_epsilon():
                primeros_alpha = {EPSILON}
            else:
                primeros_alpha = self.calcular_primeros_cadena(alpha, primeros_simbolos)

            if EPSILON not in primeros_alpha:
                conjunto_pred = set(primeros_alpha)
            else:
                conjunto_pred = (primeros_alpha - {EPSILON}) | siguientes[A]

            predicciones[regla.id] = (regla, conjunto_pred)

        return predicciones

    def verificar_ll1(self, predicciones: Dict[int, Tuple[Regla, Set[str]]]) -> Tuple[bool, List[str]]:
        """
        Verifica si la gramática es LL(1) evaluando si las reglas con la misma
        cabeza tienen conjuntos de predicción disjuntos.
        """
        es_ll1 = True
        conflictos: List[str] = []
        reglas_por_cabeza: Dict[str, List[Tuple[Regla, Set[str]]]] = {nt: [] for nt in self.no_terminales}

        for id_regla, (regla, pred) in predicciones.items():
            reglas_por_cabeza[regla.cabeza].append((regla, pred))

        for nt, lista in reglas_por_cabeza.items():
            for i in range(len(lista)):
                for j in range(i + 1, len(lista)):
                    r1, p1 = lista[i]
                    r2, p2 = lista[j]
                    interseccion = p1 & p2
                    if interseccion:
                        es_ll1 = False
                        inter_str = ", ".join(sorted(interseccion))
                        conflictos.append(
                            f"Conflicto en no terminal '{nt}' entre Regla {r1.id} [{r1}] y Regla {r2.id} [{r2}]: Intersección = {{{inter_str}}}"
                        )

        return es_ll1, conflictos
