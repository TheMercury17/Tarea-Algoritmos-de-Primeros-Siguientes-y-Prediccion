# Taller: Algoritmos de Primeros, Siguientes y Predicción

**Universidad Sergio Arboleda**  
**Escuela de Ciencias Exactas e Ingeniería**  
**Materia:** Lenguajes de Programación  
**Grupo 5:**
- **Andrés Sebastián Coral Vallejo**
- **Carol Arenas Cardona**

---

## Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Fundamento Teórico](#fundamento-teórico)
   - [Símbolos Anulables](#símbolos-anulables-nullable)
   - [Conjuntos de PRIMEROS (FIRST)](#conjuntos-de-primeros-first)
   - [Conjuntos de SIGUIENTES (FOLLOW)](#conjuntos-de-siguientes-follow)
   - [Conjuntos de PREDICCIÓN (SELECT)](#conjuntos-de-predicción-select)
   - [Condición de Gramática LL(1)](#condición-de-gramática-ll1)
3. [Ejercicio 1](#ejercicio-1)
   - [Gramática Formal](#gramática-formal-1)
   - [Desarrollo Analítico Paso a Paso](#desarrollo-analítico-paso-a-paso-1)
   - [Resultados del Algoritmo en Python](#resultados-del-algoritmo-en-python-1)
   - [Tabla Comparativa: Analítico vs Algorítmico](#tabla-comparativa-analítico-vs-algorítmico-1)
   - [Diagnóstico LL(1)](#diagnóstico-ll1-1)
4. [Ejercicio 2](#ejercicio-2)
   - [Gramática Formal](#gramática-formal-2)
   - [Desarrollo Analítico Paso a Paso](#desarrollo-analítico-paso-a-paso-2)
   - [Resultados del Algoritmo en Python](#resultados-del-algoritmo-en-python-2)
   - [Tabla Comparativa: Analítico vs Algorítmico](#tabla-comparativa-analítico-vs-algorítmico-2)
   - [Diagnóstico LL(1)](#diagnóstico-ll1-2)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Instrucciones de Ejecución](#instrucciones-de-ejecución)
7. [Pruebas Automatizadas](#pruebas-automatizadas)

---

## Descripción General

Este taller implementa y analiza los algoritmos fundamentales para el análisis sintáctico descendente predictivo:
- **Cálculo analítico** (manual y formal) de los conjuntos de **PRIMEROS**, **SIGUIENTES** y **PREDICCIÓN** para dos gramáticas libres de contexto.
- **Implementación algorítmica en Python** de dichos algoritmos siguiendo un esquema iterativo de punto fijo (*fixed-point iteration*).
- **Validación y comparación al 100%** de los resultados teóricos frente a los calculados por la máquina mediante pruebas unitarias (`unittest`).

---

## Fundamento Teórico

### Símbolos Anulables (*Nullable*)
Un símbolo no terminal $X$ es anulable ($X \Rightarrow^* \varepsilon$) si puede derivar en la cadena vacía $\varepsilon$ en uno o más pasos de derivación.

### Conjuntos de PRIMEROS (*FIRST*)
Para una secuencia de símbolos $\alpha = X_1 X_2 \dots X_n$:
1. Si $X$ es terminal, $\text{FIRST}(X) = \{X\}$.
2. Si $X \to \varepsilon$ es una regla, entonces $\varepsilon \in \text{FIRST}(X)$.
3. Para una regla $A \to Y_1 Y_2 \dots Y_k$:
   - Se agrega $\text{FIRST}(Y_1) \setminus \{\varepsilon\}$ a $\text{FIRST}(A)$.
   - Si $\varepsilon \in \text{FIRST}(Y_1)$, se agrega $\text{FIRST}(Y_2) \setminus \{\varepsilon\}$, y así sucesivamente.
   - Si todos los $Y_i$ son anulables, entonces $\varepsilon \in \text{FIRST}(A)$.

### Conjuntos de SIGUIENTES (*FOLLOW*)
Para cada no terminal $A$:
1. Se coloca el marcador de fin de entrada `$` en $\text{FOLLOW}(S)$, donde $S$ es el símbolo inicial: `$` $\in \text{FOLLOW}(S)$.
2. Si existe una producción $A \to \alpha B \beta$:
   - Todo símbolo en $\text{FIRST}(\beta) \setminus \{\varepsilon\}$ pertenece a $\text{FOLLOW}(B)$.
3. Si existe una producción $A \to \alpha B$ o $A \to \alpha B \beta$ donde $\varepsilon \in \text{FIRST}(\beta)$:
   - Todo símbolo en $\text{FOLLOW}(A)$ pertenece a $\text{FOLLOW}(B)$.

### Conjuntos de PREDICCIÓN (*PRED* o *SELECT*)
Para cada regla de producción $A \to \alpha$:
- Si $\varepsilon \notin \text{FIRST}(\alpha)$:
  $$\text{PRED}(A \to \alpha) = \text{FIRST}(\alpha)$$
- Si $\varepsilon \in \text{FIRST}(\alpha)$:
  $$\text{PRED}(A \to \alpha) = (\text{FIRST}(\alpha) \setminus \{\varepsilon\}) \cup \text{FOLLOW}(A)$$

### Condición de Gramática LL(1)
Una gramática es **LL(1)** si y solo si, para cada no terminal $A$ con producciones alternativas $A \to \alpha_1 \mid \alpha_2 \mid \dots \mid \alpha_k$, los conjuntos de predicción son mutuamente disjuntos:
$$\text{PRED}(A \to \alpha_i) \cap \text{PRED}(A \to \alpha_j) = \emptyset \quad \forall i \neq j$$

---

## Ejercicio 1

### Gramática Formal 1
- **No terminales:** $\{S, A, B, C, D\}$  
- **Terminales:** $\{\text{uno}, \text{dos}, \text{tres}, \text{cuatro}, \text{cinco}, \text{seis}\}$  
- **Símbolo inicial:** $S$

**Reglas de producción:**
1. `S -> A uno B C`
2. `S -> S dos`
3. `A -> B C D`
4. `A -> A tres`
5. `A -> ε`
6. `B -> D cuatro C tres`
7. `B -> ε`
8. `C -> cinco D B`
9. `C -> ε`
10. `D -> seis`
11. `D -> ε`

---

### Desarrollo Analítico Paso a Paso 1

#### 1. Determinación de Anulables
- `D -> ε` $\implies D$ es anulable.
- `C -> ε` $\implies C$ es anulable.
- `B -> ε` $\implies B$ es anulable.
- `A -> ε` y `A -> B C D` (con $B, C, D$ anulables) $\implies A$ es anulable.
- `S -> A uno B C` contiene el terminal `uno` y `S -> S dos` contiene `dos`, por tanto $S$ **no** es anulable.

#### 2. Cálculo de PRIMEROS
- **$D$:**
  - $D \to \text{seis} \implies \text{seis} \in \text{PRIMEROS}(D)$
  - $D \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(D)$  
  > **PRIMEROS(D)** = `{ seis, ε }`

- **$C$:**
  - $C \to \text{cinco } D B \implies \text{cinco} \in \text{PRIMEROS}(C)$
  - $C \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(C)$  
  > **PRIMEROS(C)** = `{ cinco, ε }`

- **$B$:**
  - $B \to D \text{ cuatro } C \text{ tres}$: Como $\varepsilon \in \text{PRIMEROS}(D)$, toma $(\text{PRIMEROS}(D) \setminus \{\varepsilon\}) \cup \{\text{cuatro}\} = \{\text{seis}, \text{cuatro}\}$.
  - $B \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(B)$  
  > **PRIMEROS(B)** = `{ cuatro, seis, ε }`

- **$A$:**
  - $A \to B C D$: Con $B, C, D$ anulables, aporta $(\text{PRIMEROS}(B)\setminus\{\varepsilon\}) \cup (\text{PRIMEROS}(C)\setminus\{\varepsilon\}) \cup (\text{PRIMEROS}(D)\setminus\{\varepsilon\}) \cup \{\varepsilon\} = \{\text{cuatro}, \text{seis}, \text{cinco}, \varepsilon\}$.
  - $A \to A \text{ tres}$: Dado que $A \Rightarrow^* \varepsilon$, se produce la derivación $A \Rightarrow A \text{ tres} \Rightarrow \varepsilon \text{ tres} = \text{tres}$, aportando $\text{tres} \in \text{PRIMEROS}(A)$.
  - $A \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(A)$  
  > **PRIMEROS(A)** = `{ cinco, cuatro, seis, tres, ε }`

- **$S$:**
  - $S \to A \text{ uno } B C$: Como $A$ es anulable, aporta $(\text{PRIMEROS}(A)\setminus\{\varepsilon\}) \cup \{\text{uno}\} = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$.
  - $S \to S \text{ dos}$: Aporta $\text{PRIMEROS}(S)$.  
  > **PRIMEROS(S)** = `{ cinco, cuatro, seis, tres, uno }`

#### 3. Cálculo de SIGUIENTES
- **S:** Símbolo inicial (se coloca el marcador de fin de cadena `$` en `SIGUIENTES(S)`).
  - De `S -> S dos`, sigue el terminal `dos` $\in \text{SIGUIENTES}(S)$.  
  > **SIGUIENTES(S)** = `{ $, dos }`

- **A:**
  - De `S -> A uno B C`, tras $A$ está `uno` $\implies \text{uno} \in \text{SIGUIENTES}(A)$.
  - De `A -> A tres`, tras $A$ está `tres` $\implies \text{tres} \in \text{SIGUIENTES}(A)$.  
  > **SIGUIENTES(A)** = `{ tres, uno }`

- **C:**
  - De `S -> A uno B C`: $C$ está al final, hereda `SIGUIENTES(S) = { $, dos }`.
  - De `A -> B C D`: tras $C$ está $D$; aporta $\text{PRIMEROS}(D)\setminus\{\varepsilon\} = \{\text{seis}\}$; como $D$ es anulable, hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
  - De `B -> D cuatro C tres`: tras $C$ está el terminal `tres`.  
  > **SIGUIENTES(C)** = `{ $, dos, seis, tres, uno }`

- **B:**
  - De `S -> A uno B C`: tras $B$ está $C$; aporta $\text{PRIMEROS}(C)\setminus\{\varepsilon\} = \{\text{cinco}\}$; como $C$ es anulable, hereda `SIGUIENTES(S) = { $, dos }`.
  - De `A -> B C D`: tras $B$ está $C D$; aporta $\text{PRIMEROS}(C D)\setminus\{\varepsilon\} = \{\text{cinco}, \text{seis}\}$; como $C D$ es anulable, hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
  - De `C -> cinco D B`: $B$ está al final, hereda $\text{SIGUIENTES}(C)$.  
  > **SIGUIENTES(B)** = `{ $, cinco, dos, seis, tres, uno }`

- **$D$:**
  - De `A -> B C D`: $D$ está al final, hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
  - De `B -> D cuatro C tres`: tras $D$ está `cuatro` $\in \text{SIGUIENTES}(D)$.
  - De `C -> cinco D B`: tras $D$ está $B$; aporta $\text{PRIMEROS}(B)\setminus\{\varepsilon\} = \{\text{cuatro}, \text{seis}\}$; como $B$ es anulable, hereda $\text{SIGUIENTES}(C)$.  
  > **SIGUIENTES(D)** = `{ $, cuatro, dos, seis, tres, uno }`

#### 4. Cálculo de PREDICCIÓN
| Regla | Cuerpo $\alpha$ | $\text{PRIMEROS}(\alpha)$ | ¿$\varepsilon \in \text{PRIMEROS}(\alpha)$? | Fórmula de Predicción | Conjunto de PREDICCIÓN |
|---|---|---|:---:|---|---|
| (1) `S -> A uno B C` | `A uno B C` | `{ cinco, cuatro, seis, tres, uno }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cinco, cuatro, seis, tres, uno }`** |
| (2) `S -> S dos` | `S dos` | `{ cinco, cuatro, seis, tres, uno }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cinco, cuatro, seis, tres, uno }`** |
| (3) `A -> B C D` | `B C D` | `{ cinco, cuatro, seis, ε }` | Sí | $(\text{PRIMEROS} \setminus \{\varepsilon\}) \cup \text{FOLLOW}(A)$ | **`{ cinco, cuatro, seis, tres, uno }`** |
| (4) `A -> A tres` | `A tres` | `{ cinco, cuatro, seis, tres }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cinco, cuatro, seis, tres }`** |
| (5) `A -> ε` | `ε` | `{ ε }` | Sí | $\text{FOLLOW}(A)$ | **`{ tres, uno }`** |
| (6) `B -> D cuatro C tres` | `D cuatro C tres` | `{ cuatro, seis }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cuatro, seis }`** |
| (7) `B -> ε` | `ε` | `{ ε }` | Sí | $\text{FOLLOW}(B)$ | **`{ $, cinco, dos, seis, tres, uno }`** |
| (8) `C -> cinco D B` | `cinco D B` | `{ cinco }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cinco }`** |
| (9) `C -> ε` | `ε` | `{ ε }` | Sí | $\text{FOLLOW}(C)$ | **`{ $, dos, seis, tres, uno }`** |
| (10) `D -> seis` | `seis` | `{ seis }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ seis }`** |
| (11) `D -> ε` | `ε` | `{ ε }` | Sí | $\text{FOLLOW}(D)$ | **`{ $, cuatro, dos, seis, tres, uno }`** |

---

### Resultados del Algoritmo en Python 1
Al ejecutar `python ejercicio1.py`:
- `PRIMEROS(S) = { cinco, cuatro, seis, tres, uno }`
- `PRIMEROS(A) = { cinco, cuatro, seis, tres, ε }`
- `PRIMEROS(B) = { cuatro, seis, ε }`
- `PRIMEROS(C) = { cinco, ε }`
- `PRIMEROS(D) = { seis, ε }`
- `SIGUIENTES(S) = { $, dos }`
- `SIGUIENTES(A) = { tres, uno }`
- `SIGUIENTES(B) = { $, cinco, dos, seis, tres, uno }`
- `SIGUIENTES(C) = { $, dos, seis, tres, uno }`
- `SIGUIENTES(D) = { $, cuatro, dos, seis, tres, uno }`

---

### Tabla Comparativa: Analítico vs Algorítmico 1

| Componente | No Terminal / Regla | Analítico | Algoritmo Python | Estado |
|---|---|---|---|:---:|
| **PRIMEROS** | $S$ | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **PRIMEROS** | $A$ | `{ cinco, cuatro, seis, tres, ε }` | `{ cinco, cuatro, seis, tres, ε }` | **COINCIDE** |
| **PRIMEROS** | $B$ | `{ cuatro, seis, ε }` | `{ cuatro, seis, ε }` | **COINCIDE** |
| **PRIMEROS** | $C$ | `{ cinco, ε }` | `{ cinco, ε }` | **COINCIDE** |
| **PRIMEROS** | $D$ | `{ seis, ε }` | `{ seis, ε }` | **COINCIDE** |
| **SIGUIENTES** | $S$ | `{ $, dos }` | `{ $, dos }` | **COINCIDE** |
| **SIGUIENTES** | $A$ | `{ tres, uno }` | `{ tres, uno }` | **COINCIDE** |
| **SIGUIENTES** | $B$ | `{ $, cinco, dos, seis, tres, uno }` | `{ $, cinco, dos, seis, tres, uno }` | **COINCIDE** |
| **SIGUIENTES** | $C$ | `{ $, dos, seis, tres, uno }` | `{ $, dos, seis, tres, uno }` | **COINCIDE** |
| **SIGUIENTES** | $D$ | `{ $, cuatro, dos, seis, tres, uno }` | `{ $, cuatro, dos, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (1) `S -> A uno B C` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (2) `S -> S dos` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (3) `A -> B C D` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (4) `A -> A tres` | `{ cinco, cuatro, seis, tres }` | `{ cinco, cuatro, seis, tres }` | **COINCIDE** |
| **PREDICCIÓN** | (5) `A -> ε` | `{ tres, uno }` | `{ tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (6) `B -> D cuatro C tres` | `{ cuatro, seis }` | `{ cuatro, seis }` | **COINCIDE** |
| **PREDICCIÓN** | (7) `B -> ε` | `{ $, cinco, dos, seis, tres, uno }` | `{ $, cinco, dos, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (8) `C -> cinco D B` | `{ cinco }` | `{ cinco }` | **COINCIDE** |
| **PREDICCIÓN** | (9) `C -> ε` | `{ $, dos, seis, tres, uno }` | `{ $, dos, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (10) `D -> seis` | `{ seis }` | `{ seis }` | **COINCIDE** |
| **PREDICCIÓN** | (11) `D -> ε` | `{ $, cuatro, dos, seis, tres, uno }` | `{ $, cuatro, dos, seis, tres, uno }` | **COINCIDE** |

---

### Diagnóstico LL(1) 1
La gramática **NO es LL(1)** debido a:
1. **Recursión por izquierda directa:** en `S -> S dos` y `A -> A tres`.
2. **Conflictos en los conjuntos de predicción:**
   - Para $S$: $\text{PRED}(1) \cap \text{PRED}(2) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\} \neq \emptyset$.
   - Para $A$: $\text{PRED}(3) \cap \text{PRED}(4) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}\} \neq \emptyset$; además colisionan con $\text{PRED}(5)$.
   - Para $B$: $\text{PRED}(6) \cap \text{PRED}(7) = \{\text{seis}\} \neq \emptyset$.
   - Para $D$: $\text{PRED}(10) \cap \text{PRED}(11) = \{\text{seis}\} \neq \emptyset$.

---

## Ejercicio 2

### Gramática Formal 2
- **No terminales:** $\{S, A, B, C, D\}$  
- **Terminales:** $\{\text{uno}, \text{dos}, \text{tres}, \text{cuatro}, \text{cinco}, \text{seis}\}$  
- **Símbolo inicial:** $S$

**Reglas de producción:**
1. `S -> A B uno`
2. `A -> dos B`
3. `A -> ε`
4. `B -> C D`
5. `B -> tres`
6. `B -> ε`
7. `C -> cuatro A B`
8. `C -> cinco`
9. `D -> seis`
10. `D -> ε`

---

### Desarrollo Analítico Paso a Paso 2

#### 1. Determinación de Anulables
- `D -> ε` $\implies D$ es anulable.
- `C -> cuatro A B` inicia en `cuatro`, y `C -> cinco` inicia en `cinco` $\implies C$ **no** es anulable ($\varepsilon \notin \text{PRIMEROS}(C)$).
- `B -> ε` $\implies B$ es anulable.
- `A -> ε` $\implies A$ es anulable.
- `S -> A B uno` finaliza en `uno` $\implies S$ **no** es anulable.

#### 2. Cálculo de PRIMEROS
- **$D$:**
  - $D \to \text{seis} \implies \text{seis} \in \text{PRIMEROS}(D)$
  - $D \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(D)$  
  > **PRIMEROS(D)** = `{ seis, ε }`

- **$C$:**
  - $C \to \text{cuatro } A B \implies \text{cuatro} \in \text{PRIMEROS}(C)$
  - $C \to \text{cinco} \implies \text{cinco} \in \text{PRIMEROS}(C)$  
  > **PRIMEROS(C)** = `{ cuatro, cinco }`

- **$B$:**
  - $B \to C D$: Como $C$ no es anulable, $\text{PRIMEROS}(C D) = \text{PRIMEROS}(C) = \{\text{cuatro}, \text{cinco}\}$.
  - $B \to \text{tres} \implies \text{tres} \in \text{PRIMEROS}(B)$.
  - $B \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(B)$.  
  > **PRIMEROS(B)** = `{ cinco, cuatro, tres, ε }`

- **$A$:**
  - $A \to \text{dos } B \implies \text{dos} \in \text{PRIMEROS}(A)$.
  - $A \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(A)$.  
  > **PRIMEROS(A)** = `{ dos, ε }`

- **$S$:**
  - $S \to A B \text{ uno}$:
    - Aporta $\text{PRIMEROS}(A)\setminus\{\varepsilon\} = \{\text{dos}\}$.
    - Como $A$ es anulable, aporta $\text{PRIMEROS}(B)\setminus\{\varepsilon\} = \{\text{cinco}, \text{cuatro}, \text{tres}\}$.
    - Como $B$ también es anulable, aporta el siguiente terminal $\{\text{uno}\}$.  
  > **PRIMEROS(S)** = `{ cinco, cuatro, dos, tres, uno }`

#### 3. Cálculo de SIGUIENTES
- **S:** Símbolo inicial (se coloca el marcador de fin de cadena `$` en `SIGUIENTES(S)`). Como $S$ no aparece en el cuerpo de ninguna regla:  
  > **SIGUIENTES(S)** = `{ $ }`

- **Propagación mutua entre $A, B, C, D$:**
  1. De `S -> A B uno`:
     - Tras $A$ está $B \text{ uno} \implies \text{PRIMEROS}(B \text{ uno})\setminus\{\varepsilon\} = \{\text{tres}, \text{cuatro}, \text{cinco}, \text{uno}\} \subseteq \text{SIGUIENTES}(A)$.
     - Tras $B$ está el terminal `uno` $\implies \text{uno} \in \text{SIGUIENTES}(B)$.
  2. De `A -> dos B`:
     - $B$ está al final $\implies \text{SIGUIENTES}(A) \subseteq \text{SIGUIENTES}(B)$.
  3. De `C -> cuatro A B`:
     - Tras $A$ está $B \implies \text{PRIMEROS}(B)\setminus\{\varepsilon\} \subseteq \text{SIGUIENTES}(A)$, y al ser $B$ anulable, $\text{SIGUIENTES}(C) \subseteq \text{SIGUIENTES}(A)$.
     - $B$ está al final $\implies \text{SIGUIENTES}(C) \subseteq \text{SIGUIENTES}(B)$.
  4. De `B -> C D`:
     - Tras $C$ está $D \implies \text{PRIMEROS}(D)\setminus\{\varepsilon\} = \{\text{seis}\} \subseteq \text{SIGUIENTES}(C)$.
     - Como $D$ es anulable, $\text{SIGUIENTES}(B) \subseteq \text{SIGUIENTES}(C)$.
     - $D$ está al final $\implies \text{SIGUIENTES}(B) \subseteq \text{SIGUIENTES}(D)$.
  
  **Resolución del sistema cerrado:**
  - $\text{SIGUIENTES}(C)$ recibe $\{\text{seis}\} \cup \text{SIGUIENTES}(B)$.
  - $\text{SIGUIENTES}(B)$ recibe $\text{SIGUIENTES}(A) \cup \text{SIGUIENTES}(C)$.
  - $\text{SIGUIENTES}(A)$ recibe $\{\text{uno}, \text{tres}, \text{cuatro}, \text{cinco}\} \cup \text{SIGUIENTES}(C)$.
  
  Por tanto, $A, B, C$ y $D$ convergen al mismo conjunto unión:
  > **SIGUIENTES(A)** = `{ cinco, cuatro, seis, tres, uno }`  
  > **SIGUIENTES(B)** = `{ cinco, cuatro, seis, tres, uno }`  
  > **SIGUIENTES(C)** = `{ cinco, cuatro, seis, tres, uno }`  
  > **SIGUIENTES(D)** = `{ cinco, cuatro, seis, tres, uno }`  

*(Nota: el símbolo de fin de cadena `$` no se propaga a ningún otro no terminal porque la regla `S -> A B uno` termina estrictamente con el terminal `uno`).*

#### 4. Cálculo de PREDICCIÓN
| Regla | Cuerpo $\alpha$ | $\text{PRIMEROS}(\alpha)$ | ¿$\varepsilon \in \text{PRIMEROS}(\alpha)$? | Fórmula de Predicción | Conjunto de PREDICCIÓN |
|---|---|---|:---:|---|---|
| (1) `S -> A B uno` | `A B uno` | `{ cinco, cuatro, dos, tres, uno }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cinco, cuatro, dos, tres, uno }`** |
| (2) `A -> dos B` | `dos B` | `{ dos }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ dos }`** |
| (3) `A -> ε` | `ε` | `{ ε }` | Sí | $\text{FOLLOW}(A)$ | **`{ cinco, cuatro, seis, tres, uno }`** |
| (4) `B -> C D` | `C D` | `{ cinco, cuatro }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cinco, cuatro }`** |
| (5) `B -> tres` | `tres` | `{ tres }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ tres }`** |
| (6) `B -> ε` | `ε` | `{ ε }` | Sí | $\text{FOLLOW}(B)$ | **`{ cinco, cuatro, seis, tres, uno }`** |
| (7) `C -> cuatro A B` | `cuatro A B` | `{ cuatro }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cuatro }`** |
| (8) `C -> cinco` | `cinco` | `{ cinco }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ cinco }`** |
| (9) `D -> seis` | `seis` | `{ seis }` | No | $\text{PRIMEROS}(\alpha)$ | **`{ seis }`** |
| (10) `D -> ε` | `ε` | `{ ε }` | Sí | $\text{FOLLOW}(D)$ | **`{ cinco, cuatro, seis, tres, uno }`** |

---

### Resultados del Algoritmo en Python 2
Al ejecutar `python ejercicio2.py`:
- `PRIMEROS(S) = { cinco, cuatro, dos, tres, uno }`
- `PRIMEROS(A) = { dos, ε }`
- `PRIMEROS(B) = { cinco, cuatro, tres, ε }`
- `PRIMEROS(C) = { cinco, cuatro }`
- `PRIMEROS(D) = { seis, ε }`
- `SIGUIENTES(S) = { $ }`
- `SIGUIENTES(A) = { cinco, cuatro, seis, tres, uno }`
- `SIGUIENTES(B) = { cinco, cuatro, seis, tres, uno }`
- `SIGUIENTES(C) = { cinco, cuatro, seis, tres, uno }`
- `SIGUIENTES(D) = { cinco, cuatro, seis, tres, uno }`

---

### Tabla Comparativa: Analítico vs Algorítmico 2

| Componente | No Terminal / Regla | Analítico | Algoritmo Python | Estado |
|---|---|---|---|:---:|
| **PRIMEROS** | $S$ | `{ cinco, cuatro, dos, tres, uno }` | `{ cinco, cuatro, dos, tres, uno }` | **COINCIDE** |
| **PRIMEROS** | $A$ | `{ dos, ε }` | `{ dos, ε }` | **COINCIDE** |
| **PRIMEROS** | $B$ | `{ cinco, cuatro, tres, ε }` | `{ cinco, cuatro, tres, ε }` | **COINCIDE** |
| **PRIMEROS** | $C$ | `{ cinco, cuatro }` | `{ cinco, cuatro }` | **COINCIDE** |
| **PRIMEROS** | $D$ | `{ seis, ε }` | `{ seis, ε }` | **COINCIDE** |
| **SIGUIENTES** | $S$ | `{ $ }` | `{ $ }` | **COINCIDE** |
| **SIGUIENTES** | $A$ | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **SIGUIENTES** | $B$ | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **SIGUIENTES** | $C$ | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **SIGUIENTES** | $D$ | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (1) `S -> A B uno` | `{ cinco, cuatro, dos, tres, uno }` | `{ cinco, cuatro, dos, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (2) `A -> dos B` | `{ dos }` | `{ dos }` | **COINCIDE** |
| **PREDICCIÓN** | (3) `A -> ε` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (4) `B -> C D` | `{ cinco, cuatro }` | `{ cinco, cuatro }` | **COINCIDE** |
| **PREDICCIÓN** | (5) `B -> tres` | `{ tres }` | `{ tres }` | **COINCIDE** |
| **PREDICCIÓN** | (6) `B -> ε` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |
| **PREDICCIÓN** | (7) `C -> cuatro A B` | `{ cuatro }` | `{ cuatro }` | **COINCIDE** |
| **PREDICCIÓN** | (8) `C -> cinco` | `{ cinco }` | `{ cinco }` | **COINCIDE** |
| **PREDICCIÓN** | (9) `D -> seis` | `{ seis }` | `{ seis }` | **COINCIDE** |
| **PREDICCIÓN** | (10) `D -> ε` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **COINCIDE** |

---

### Diagnóstico LL(1) 2
La gramática **NO es LL(1)** debido a conflictos de predicción en no terminales alternativos:
- Para $A$: $\text{PRED}(2) \cap \text{PRED}(3) = \{\text{dos}\} \cap \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\} = \emptyset$ (Disjunto - Sin conflicto).
- Para $B$:
  - $\text{PRED}(4) \cap \text{PRED}(6) = \{\text{cinco}, \text{cuatro}\} \neq \emptyset$ (Conflicto).
  - $\text{PRED}(5) \cap \text{PRED}(6) = \{\text{tres}\} \neq \emptyset$ (Conflicto).
- Para $C$: $\text{PRED}(7) \cap \text{PRED}(8) = \{\text{cuatro}\} \cap \{\text{cinco}\} = \emptyset$ (Disjunto - Sin conflicto).
- Para $D$: $\text{PRED}(9) \cap \text{PRED}(10) = \{\text{seis}\} \neq \emptyset$ (Conflicto).

---

## Estructura del Proyecto

```text
Tarea - Algoritmos de Primeros Siguientes y Prediccion/
│
├── gramatica.py            # Motor formal: clase Gramatica y algoritmos de punto fijo
├── ejercicio1.py           # Definición, solución analítica y ejecución del Ejercicio 1
├── ejercicio2.py           # Definición, solución analítica y ejecución del Ejercicio 2
├── main.py                 # Comparativa general con tablas en consola
├── test_algoritmos.py      # Suite de pruebas unitarias automatizadas (unittest)
├── Tarea - Ejercicio1.png  # Imagen del enunciado del Ejercicio 1
├── Tarea - Ejercicio2.png  # Imagen del enunciado del Ejercicio 2
└── README.md               # Informe teórico y comparativo completo
```

---

## Instrucciones de Ejecución

Para ejecutar el programa principal y visualizar las tablas comparativas:

```bash
python main.py
```

Para ejecutar cada ejercicio de forma individual:

```bash
python ejercicio1.py
python ejercicio2.py
```

---

## Pruebas Automatizadas

Para validar matemáticamente que la implementación algorítmica y la solución analítica coinciden al 100%:

```bash
python test_algoritmos.py
```

Salida esperada:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```
