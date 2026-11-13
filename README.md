# BFS 0-1 — Caminos Mínimos con Pesos 0/1

**Proyecto**: CS2023 "Anima tu Algoritmo o Estructura de Datos" (UTEC)
**Deadline**: 18/11/2026, 20:00
**Grupo**: Hasta 3 personas

---

## ¿Qué es BFS 0-1?

Es una variante de BFS para grafos **dirigidos y ponderados** cuyas aristas
solo pueden pesar **0 o 1**. Calcula la distancia mínima desde un nodo fuente
hacia todos los demás en **O(|V| + |E|)**, sin necesitar un heap como Dijkstra.

**La idea**: en vez de una cola simple, se usa un `deque`:
- Si la arista relajada pesa **0**, el vecino entra al deque por el **frente**
  (`push_front`) — se procesa antes, porque no suma distancia.
- Si pesa **1**, entra por **atrás** (`push_back`) — se procesa después.

Así el deque se mantiene ordenado por distancia sin ordenar nada explícitamente.

### ¿Para qué sirve?
- Caminos mínimos cuando los pesos son binarios (ej: "¿cuesta cambiar de
  estado o no?", grafos de capas 0/1 en problemas de grillas).
- Es un punto medio entre BFS normal (no soporta pesos) y Dijkstra genérico
  (más lento, necesita un heap).

---

## Estructura del Proyecto

```
BFS_0-1/
├── include/bfs01/
│   └── bfs01.h                 # Contrato (interfaz que usan todos)
├── src/bfs01/
│   ├── graph_core.cpp          # buildGraph() + emit() — Persona 0
│   ├── init.cpp                # initBFS01() — Persona 1 ✅
│   └── bfs01.cpp               # bfs01() — Persona 2 (por hacer)
├── src/
│   ├── demo_cases.cpp          # Grafo de ejemplo + caso borde — Persona 3 (por hacer)
│   └── main.cpp                # Integra todo — Persona 3 (por hacer)
├── tests/
│   └── test_infra.cpp          # Prueba aislada de buildGraph()/emit()
├── animation/
│   └── render_bfs01.py         # Script Manim — Persona 3 (por hacer)
├── CMakeLists.txt              # Instrucciones para compilar
├── README.md                   # Este archivo
└── trace.jsonl                 # Output: "película" del algoritmo (generado, no se versiona)
```

---

## Estado del Trabajo

### ✅ Listo (Denilson — Infraestructura)

**`bfs01.h`** — El contrato compartido:
- Variables globales: `adj` (lista de adyacencia dirigida), `dist`, `visited`, `dq`.
- `buildGraph(n, edges)`: arma el grafo a partir de triples `(u, v, peso)`.
- `emit(event, note, currentNode)`: fotografía el estado actual.
- Declara `initBFS01()` y `bfs01()` para que Persona 1 y 2 las implementen
  sin tocar este archivo.

**`graph_core.cpp`** — Las "cámaras":
- `buildGraph()`: resetea `adj`/`dist`/`visited`/`dq` y carga las aristas
  (grafo dirigido: cada arista solo va `u -> v`).
- `emit()`: recorre `dist[]`/`visited[]` de todos los nodos + el contenido
  actual del `deque`, y escribe una línea JSON a `trace.jsonl`. No conoce la
  lógica del algoritmo, solo registra lo que le pasan.
- `dist[i] == -1` significa "no alcanzado todavía" (equivalente a infinito).

**`CMakeLists.txt`** — Configuración para compilar:
- Funciona en Windows (Visual Studio/MSVC), Linux (g++), Mac (clang).
- Ya compila un ejecutable de prueba (`test_infra`) con la infraestructura.
- Deja comentadas las líneas que cada persona debe descomentar al entregar
  su archivo (ver sección "Quién hace qué" más abajo).

**`tests/test_infra.cpp`** — Prueba de humo:
- Construye un grafo de 4 nodos y simula a mano un par de pasos del
  algoritmo (sin depender de `initBFS01()`/`bfs01()`, que todavía no existen)
  para confirmar que `buildGraph()` y `emit()` generan el `trace.jsonl`
  esperado.

### ✅ Listo (Persona 1 — `feature/init`)

**`src/bfs01/init.cpp`**:
- `initBFS01(source)`: `dist[source] = 0` y `dq.push_front(source)`.
  `visited`/`dist` del resto ya quedan en `-1`/`false` desde `buildGraph()`.
- Llama a `emit()` para registrar el estado inicial.
- `tests/test_init.cpp`: prueba aislada (no depende de `bfs01()`, que
  todavía no existe).

⏳ Falta grabar: intro conceptual (~30s) — para qué sirve BFS 0-1, por qué
BFS normal no funciona con pesos 0/1, representación del grafo.

---

### ⏳ Por Hacer (Persona 2 — `feature/bfs01-algoritmo`)

**`src/bfs01/bfs01.cpp`**:
- [ ] `bfs01(source)`: llama a `initBFS01(source)` y corre el `while` principal:
      `pop_front` del deque, marcar `visited`, relajar cada arista saliente
      (si mejora `dist[v]`, actualizar y hacer `push_front` si peso 0 /
      `push_back` si peso 1).
- [ ] Usar `emit()` en cada paso relevante (pop, relax, descarte de nodo
      ya visitado).
- [ ] En el video: demo animada del algoritmo paso a paso (~45-50s).

---

### ⏳ Por Hacer (Persona 3 — `feature/casos-integracion`)

**`src/demo_cases.cpp` + `src/main.cpp`**:
- [ ] Grafo de ejemplo ilustrativo (nodos + aristas + pesos a elegir).
- [ ] Al menos un caso borde (nodo inalcanzable, un solo nodo, o todas las
      aristas de peso 1).
- [ ] `main()` que llama a `buildGraph()` + `bfs01()` sobre ambos grafos.
- [ ] Habilitar el target `bfs01_demo` en `CMakeLists.txt` (descomentar las
      líneas ya dejadas listas).

**`animation/render_bfs01.py`**:
- [ ] Adaptar el script de Manim (o escribir uno nuevo) para leer
      `trace.jsonl` con el nuevo formato (nodos con `dist`/`visited` + deque,
      ya no es un árbol con padres/hijos).
- [ ] Resaltar `current_node` y mostrar `note` como subtítulo.
- [ ] Exportar a video `.mp4`.
- [ ] En el video: caso borde + análisis de complejidad (BFS 0-1 O(V+E) vs.
      Dijkstra genérico O((V+E)·log V)) + créditos (~35s).

---

## Cómo Compilar y Ejecutar

### Necesitas:
- CMake 3.10 o más nuevo.
- Compilador C++ que entienda C++17 (g++, clang, MSVC).

### En Linux o Mac:
```bash
cd BFS_0-1
mkdir build && cd build
cmake ..
cmake --build .
./test_infra
```

### En Windows (Visual Studio):
```bash
cd BFS_0-1
mkdir build && cd build
cmake .. -G "Visual Studio 17 2022"
cmake --build . --config Debug
.\Debug\test_infra.exe
```

**Resultado esperado**: se genera `trace.jsonl` con 3 líneas JSON (una por
cada llamada a `emit()` en la prueba).

Cuando Persona 3 integre todo, el target `bfs01_demo` (ya dejado comentado en
`CMakeLists.txt`) correrá el algoritmo real sobre el grafo de ejemplo y el
caso borde.

---

## Formato de `trace.jsonl`

Una línea JSON por evento. Cada línea tiene: el evento, una nota en texto
(subtítulo del video), el nodo resaltado, el snapshot de todos los nodos
(`dist`/`visited`) y el contenido actual del deque.

```json
{"event":"init","note":"Nodo 0 marcado como fuente, dist=0","current_node":0,"nodes":[{"id":0,"dist":0,"visited":true},{"id":1,"dist":-1,"visited":false},{"id":2,"dist":-1,"visited":false},{"id":3,"dist":-1,"visited":false}],"deque":[0]}
```

Manim procesa esto línea por línea y anima las transiciones (nodo que entra
al deque por el frente o por atrás, cambios de color al visitarse, etc.).

---

## Quién Hace Qué

| Parte | Persona | Archivo(s) | Explica en el video |
|---|---|---|---|
| 0. Infraestructura | Denilson | `bfs01.h`, `graph_core.cpp`, `CMakeLists.txt` ✅ | — |
| 1. Inicialización + intro | Persona 1 | `init.cpp` | Intro conceptual (~30s) |
| 2. Algoritmo central | Persona 2 | `bfs01.cpp` | Demo animada paso a paso (~45-50s) |
| 3. Casos + integración | Persona 3 | `demo_cases.cpp`, `main.cpp`, `render_bfs01.py` | Caso borde + complejidad + créditos (~35s) |

---

## Flujo de Git

1. `bfs01.h` + `graph_core.cpp` + `CMakeLists.txt` + `README.md` van a `main`
   primero (Fase 0 — esto).
2. Ramas: `feature/init`, `feature/bfs01-algoritmo`, `feature/casos-integracion`.
3. Orden de merge: `init` → `bfs01-algoritmo` → `casos-integracion` (esta
   última junta todo y corre Manim).
4. Revisión cruzada de PRs entre los 3.

---

## Importante: Animación Real (No Simulada)

El enunciado exige que la animación esté **impulsada por una implementación
real** de BFS 0-1, programada por el grupo — no se permite animar "a mano" ni
usar una librería ya existente del algoritmo.

**Nuestro enfoque cumple**: C++ real → `emit()` registra eventos reales →
`trace.jsonl` tiene datos reales → Manim anima basándose en esos datos.

**No permitido**: animar valores ficticios, usar una implementación de
terceros (stdlib, librería de grafos), o falsificar los eventos.

---

## Checklist Antes de Gradescope

### Código
- [ ] Compila sin errores ni warnings
- [ ] `trace.jsonl` se genera correctamente
- [ ] Se ejecuta sin crashes
- [ ] Repositorio GitHub actualizado
- [ ] README.md con instrucciones funcionales

### Video
- [ ] Duración: 1-2 minutos (máx 5)
- [ ] Incluye intro conceptual
- [ ] Muestra la ejecución animada sobre el grafo de ejemplo
- [ ] Incluye al menos un caso borde
- [ ] Incluye análisis de complejidad
- [ ] Tiene créditos con nombres
- [ ] Formato: .mp4 (o link si pesa mucho)

### Informe PDF
- [ ] Carátula (curso, nombres, fecha)
- [ ] Descripción del algoritmo
- [ ] Herramientas usadas
- [ ] Pasos para compilar y ejecutar
- [ ] Contribución de cada integrante
- [ ] Análisis de complejidad
- [ ] Link a GitHub (funciona ✓)
- [ ] Link a video (funciona ✓)
- [ ] 2+ conclusiones escritas

### Entrega
- [ ] Solo una persona sube a Gradescope
- [ ] Incluye: código + PDF + video (o links)
- [ ] Antes de 18/11/2026 20:00
- [ ] Verifica que se subió correctamente
