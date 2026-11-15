"""
Animacion de BFS 0-1 con Manim, impulsada por trace.jsonl (generado por bfs01_demo).

Uso (desde la raiz del repo, despues de correr ./build/bfs01_demo):
    manim -qm animation/render_bfs01.py BFS01Video          # video completo
    manim -qm animation/render_bfs01.py EjemploScene        # solo el grafo de ejemplo
    manim -qm animation/render_bfs01.py CasoBordeScene      # solo los casos borde
    manim -qm animation/render_bfs01.py ComplejidadScene
    manim -qm animation/render_bfs01.py CreditosScene

Calidad: -ql (rapido), -qm (720p), -qh (1080p). El .mp4 queda en media/videos/.
El trace se busca en $BFS01_TRACE, ./trace.jsonl o ./build/trace.jsonl.

Todo lo que se dibuja sale del trace: el grafo del evento "graph", y cada paso
(init/pop/relax/keep/skip/done) con su snapshot de dist/visited/deque.
"""

import json
import math
import os
from pathlib import Path

from manim import (
    BLUE, DOWN, GRAY, GREEN, LEFT, ORANGE, RED, RIGHT, UP, WHITE, YELLOW,
    Arrow, Circle, Create, CurvedArrow, FadeIn, FadeOut, Indicate, LaggedStart,
    Line, RoundedRectangle, Scene, Square, Text, Transform, VGroup,
    Write, config,
)

# ---------------------------------------------------------------- configuracion

CREDITOS = [
    ("Infraestructura", "Denilson"),
    ("Inicializacion + intro", "Persona 1"),
    ("Algoritmo central", "Persona 2"),
    ("Casos + integracion + animacion", "Persona 3"),
]
CURSO = "CS2023 - Algoritmos y Estructuras de Datos - UTEC"

# Posiciones a mano para que los grafos de demo se lean bien.
# Cualquier otro grafo usa un layout circular automatico.
POSICIONES = {
    "ejemplo": [(-5, 0), (-2, 1.5), (-2, -1.5), (1, 1.5), (1, -1.5), (4, 0)],
    "inalcanzable": [(-4.5, 0), (-1.5, 1.4), (-1.5, -1.4), (2.5, 1.4), (2.5, -1.4)],
    "todo peso 1": [(-5, 0), (-2.5, 1.4), (-2.5, -1.4), (0.5, 0), (3.5, 0)],
}

FONT = "Helvetica"
GRAPH_SHIFT = UP * 0.7       # el grafo vive en la mitad superior
GRAPH_SCALE = 0.85
NODE_R = 0.38
COLOR_W0 = BLUE              # aristas de peso 0
COLOR_W1 = ORANGE            # aristas de peso 1
COLOR_EN_DEQUE = YELLOW
COLOR_VISITADO = GREEN
COLOR_FUENTE = RED

# Tiempos (segundos) por tipo de evento
PAUSA = {"init": 1.0, "pop": 0.8, "relax": 1.0, "keep": 0.8, "skip": 0.9, "done": 1.6}


def T(texto, size=28, color=WHITE, **kw):
    return Text(texto, font=FONT, font_size=size, color=color, **kw)


# ---------------------------------------------------------------- lectura del trace

def buscar_trace():
    candidatos = [os.environ.get("BFS01_TRACE"), "trace.jsonl", "build/trace.jsonl",
                  str(Path(__file__).resolve().parent.parent / "build" / "trace.jsonl")]
    for c in candidatos:
        if c and Path(c).is_file():
            return Path(c)
    raise FileNotFoundError("No encontre trace.jsonl: corre primero ./build/bfs01_demo "
                            "o define BFS01_TRACE")


def leer_escenas():
    """Devuelve [(evento_graph, [eventos del algoritmo]), ...] en orden."""
    escenas = []
    with open(buscar_trace(), encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            ev = json.loads(linea)
            if ev["event"] == "graph":
                escenas.append((ev, []))
            elif escenas:
                escenas[-1][1].append(ev)
    return escenas


def escena(nombre):
    for g, evs in leer_escenas():
        if g["name"] == nombre:
            return g, evs
    raise KeyError(f"El trace no tiene un grafo llamado '{nombre}'")


# ---------------------------------------------------------------- dibujo

def posiciones(g):
    n = g["n"]
    if g["name"] in POSICIONES and len(POSICIONES[g["name"]]) == n:
        pts = POSICIONES[g["name"]]
    else:
        pts = [(3 * math.cos(2 * math.pi * i / n + math.pi), 1.8 * math.sin(2 * math.pi * i / n + math.pi))
               for i in range(n)]
    return [(x * GRAPH_SCALE * RIGHT + y * GRAPH_SCALE * UP) + GRAPH_SHIFT for x, y in pts]


class GrafoVisual:
    """Nodos (circulo + id + etiqueta de distancia) y aristas dirigidas con peso."""

    def __init__(self, g):
        self.pos = posiciones(g)
        self.nodos, self.ids, self.dists = [], [], []
        for i, p in enumerate(self.pos):
            c = Circle(radius=NODE_R, color=WHITE, stroke_width=3).move_to(p)
            c.set_fill(GRAY, opacity=0.25)
            self.nodos.append(c)
            self.ids.append(T(str(i), 30).move_to(p))
            self.dists.append(self._etiqueta_dist(i, -1))

        pares = {(e["u"], e["v"]) for e in g["edges"]}
        self.aristas = {}
        for e in g["edges"]:
            u, v, w = e["u"], e["v"], e["w"]
            color = COLOR_W0 if w == 0 else COLOR_W1
            a, b = self.pos[u], self.pos[v]
            if (v, u) in pares:
                # si existe la arista inversa, curvamos para que no se encimen
                d = (b - a) / max(1e-6, _norm(b - a))
                flecha = CurvedArrow(a + d * NODE_R, b - d * NODE_R, angle=-0.5,
                                     color=color, stroke_width=4, tip_length=0.2)
            else:
                flecha = Arrow(a, b, buff=NODE_R + 0.02, color=color, stroke_width=4,
                               max_tip_length_to_length_ratio=0.12)
            medio = flecha.point_from_proportion(0.5)
            peso = T(str(w), 24, color=color)
            peso.add_background_rectangle(opacity=0.85, buff=0.06)
            peso.move_to(medio)
            self.aristas[(u, v)] = (flecha, peso, color)

    def _etiqueta_dist(self, i, d):
        texto = "d = inf" if d == -1 else f"d = {d}"
        # nodos de la fila de arriba llevan la etiqueta encima, el resto debajo,
        # asi no choca con las aristas verticales
        lado = UP if self.pos[i][1] > GRAPH_SHIFT[1] + 0.3 else DOWN
        return T(texto, 20, color=GRAY if d == -1 else WHITE).next_to(self.pos[i], lado, buff=NODE_R + 0.08)

    def mobjects(self):
        flechas = [VGroup(f, p) for f, p, _ in self.aristas.values()]
        nodos = [VGroup(c, t) for c, t in zip(self.nodos, self.ids)]
        return VGroup(*flechas), VGroup(*nodos), VGroup(*self.dists)


def _norm(v):
    return math.sqrt(float(v[0]) ** 2 + float(v[1]) ** 2)


class DequeVisual:
    """Fila de cajitas en la parte baja: frente a la izquierda, atras a la derecha."""

    Y = -3.05
    LADO = 0.62

    def __init__(self, scene):
        self.scene = scene
        self.cajas = []  # VGroup(cuadrado, numero) en el mismo orden que el deque
        etiqueta = T("deque", 24, color=GRAY).move_to(LEFT * 6.1 + UP * self.Y)
        self.front = T("frente", 18, color=COLOR_W0).move_to(LEFT * 4.9 + UP * (self.Y + 0.55))
        self.back = T("<- atras", 18, color=COLOR_W1)
        self.marco = Line(LEFT * 5.3 + UP * (self.Y - 0.42), RIGHT * 6.6 + UP * (self.Y - 0.42), color=GRAY)
        self.fijos = VGroup(etiqueta, self.front, self.marco)
        self.front.shift(UP * 0.1)
        self._ubicar_back(0)

    def _x(self, i):
        return -4.9 + i * (self.LADO + 0.1)

    def _pos_back(self, n):
        # a la derecha de la ultima caja (o del primer hueco si esta vacio)
        x = self._x(n - 1) + self.LADO / 2 + 0.55 if n > 0 else self._x(0)
        return RIGHT * x + UP * self.Y

    def _ubicar_back(self, n):
        self.back.move_to(self._pos_back(n))

    def _caja(self, valor, i):
        sq = Square(self.LADO, color=COLOR_EN_DEQUE, stroke_width=3).set_fill(COLOR_EN_DEQUE, 0.15)
        return VGroup(sq, T(str(valor), 24)).move_to(RIGHT * self._x(i) + UP * self.Y)

    def mobjects(self):
        return VGroup(self.fijos, self.back)

    def animar(self, viejo, nuevo, side):
        """Anima el paso de `viejo` a `nuevo` (listas de ids). Devuelve animaciones."""
        anims = []
        if nuevo == viejo:
            return anims
        if len(nuevo) == len(viejo) - 1 and nuevo == viejo[1:]:
            # pop_front
            sale = self.cajas.pop(0)
            anims.append(FadeOut(sale, shift=UP * 0.6))
        elif len(nuevo) == len(viejo) + 1 and side == "front" and nuevo[1:] == viejo:
            caja = self._caja(nuevo[0], 0)
            self.cajas.insert(0, caja)
            anims.append(FadeIn(caja, shift=RIGHT * 0.8))
        elif len(nuevo) == len(viejo) + 1 and nuevo[:-1] == viejo:
            caja = self._caja(nuevo[-1], len(nuevo) - 1)
            self.cajas.append(caja)
            anims.append(FadeIn(caja, shift=LEFT * 0.8))
        else:
            # cambio raro: reconstruimos todo
            anims += [FadeOut(c) for c in self.cajas]
            self.cajas = [self._caja(v, i) for i, v in enumerate(nuevo)]
            anims += [FadeIn(c) for c in self.cajas]
            anims.append(self.back.animate.move_to(self._pos_back(len(nuevo))))
            return anims
        for i, c in enumerate(self.cajas):
            anims.append(c.animate.move_to(RIGHT * self._x(i) + UP * self.Y))
        anims.append(self.back.animate.move_to(self._pos_back(len(nuevo))))
        return anims


# ---------------------------------------------------------------- escena base

class BFS01Base(Scene):

    def titulo(self, texto, sub=None):
        t = T(texto, 40).to_edge(UP, buff=0.3)
        grupo = VGroup(t)
        if sub:
            grupo.add(T(sub, 22, color=GRAY).next_to(t, DOWN, buff=0.1))
        return grupo

    def leyenda(self):
        items = [(COLOR_W0, "peso 0 -> frente"), (COLOR_W1, "peso 1 -> atras"),
                 (COLOR_EN_DEQUE, "en deque"), (COLOR_VISITADO, "visitado")]
        filas = VGroup()
        for color, txt in items:
            filas.add(VGroup(Square(0.22, color=color).set_fill(color, 0.6), T(txt, 16)).arrange(RIGHT, buff=0.12))
        return filas.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UP + RIGHT, buff=0.3).shift(DOWN * 0.9)

    def animar_grafo(self, g, eventos, titulo, sub=None):
        cab = self.titulo(titulo, sub)
        gv = GrafoVisual(g)
        flechas, nodos, dists = gv.mobjects()
        dq = DequeVisual(self)
        leyenda = self.leyenda()

        self.play(FadeIn(cab, shift=DOWN * 0.3))
        self.play(LaggedStart(*[Create(n) for n in nodos], lag_ratio=0.1), run_time=1.0)
        self.play(LaggedStart(*[Create(f) for f in flechas], lag_ratio=0.1),
                  FadeIn(dists), FadeIn(leyenda), FadeIn(dq.mobjects()), run_time=1.2)

        nota = T(" ", 26).move_to(DOWN * 2.05)
        self.add(nota)
        anillo = None
        deque_prev = []
        fuente = None
        estado = {}  # id -> (stroke, fill) ya aplicados

        for ev in eventos:
            anims = []
            tipo = ev["event"]

            # subtitulo
            nueva_nota = T(ev["note"], 26, color=YELLOW if tipo in ("relax", "init") else WHITE)
            if nueva_nota.width > 12.5:
                nueva_nota.scale_to_fit_width(12.5)
            nueva_nota.move_to(DOWN * 2.05)
            anims.append(Transform(nota, nueva_nota))

            # colores de nodos y etiquetas de distancia segun el snapshot
            en_deque = set(ev["deque"])
            for nd in ev["nodes"]:
                i, d, vis = nd["id"], nd["dist"], nd["visited"]
                color = COLOR_VISITADO if vis else (COLOR_EN_DEQUE if i in en_deque else WHITE)
                fill = COLOR_VISITADO if vis else (COLOR_EN_DEQUE if i in en_deque else GRAY)
                if estado.get(i) != (color, fill):
                    estado[i] = (color, fill)
                    anims.append(gv.nodos[i].animate.set_stroke(color).set_fill(fill, 0.45 if vis else 0.25))
                etiqueta = gv._etiqueta_dist(i, d)
                if etiqueta.text != gv.dists[i].text:
                    anims.append(Transform(gv.dists[i], etiqueta))
                    gv.dists[i].text = etiqueta.text

            # nodo actual
            cur = ev["current_node"]
            if tipo == "init":
                fuente = cur
                anims.append(gv.ids[cur].animate.set_color(COLOR_FUENTE))
            if cur is not None and cur >= 0:
                nuevo_anillo = Circle(radius=NODE_R + 0.12, color=RED, stroke_width=5).move_to(gv.pos[cur])
                if anillo is None:
                    anillo = nuevo_anillo
                    anims.append(Create(anillo))
                else:
                    anims.append(anillo.animate.move_to(gv.pos[cur]).set_stroke(RED, 5, opacity=1))
            elif anillo is not None:
                anims.append(anillo.animate.set_stroke(opacity=0))

            # deque
            anims += dq.animar(deque_prev, ev["deque"], ev["side"])
            deque_prev = ev["deque"]

            self.play(*anims, run_time=0.7)

            # arista revisada: un destello sobre la flecha
            if ev["edge"]:
                e = ev["edge"]
                flecha, peso, color = gv.aristas[(e["u"], e["v"])]
                resalte = RED if tipo == "keep" else YELLOW
                self.play(Indicate(peso, color=resalte, scale_factor=1.4),
                          flecha.animate.set_stroke(resalte, 7), run_time=0.5)
                self.play(flecha.animate.set_stroke(color, 4), run_time=0.2)
            if tipo == "skip":
                self.play(Indicate(gv.nodos[cur], color=RED), run_time=0.5)

            self.wait(PAUSA.get(tipo, 0.6))

        # resumen final
        if anillo is not None:
            self.play(FadeOut(anillo))
        finales = eventos[-1]["nodes"] if eventos else []
        inalc = [str(nd["id"]) for nd in finales if nd["dist"] == -1]
        if inalc:
            msg = T(f"Nodos inalcanzables desde {fuente}: {', '.join(inalc)}  (dist = infinito)", 26, color=RED)
            msg.move_to(DOWN * 2.05)
            self.play(Transform(nota, msg),
                      *[Indicate(gv.nodos[int(i)], color=RED) for i in inalc])
            self.wait(1.5)
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ---------------------------------------------------------------- escenas

class EjemploScene(BFS01Base):
    def construct(self):
        g, evs = escena("ejemplo")
        self.animar_grafo(g, evs, "BFS 0-1 sobre el grafo de ejemplo",
                          "aristas dirigidas con peso 0 (azul) o 1 (naranja), fuente = 0")


class CasoBordeScene(BFS01Base):
    def construct(self):
        g, evs = escena("inalcanzable")
        self.animar_grafo(g, evs, "Caso borde: nodos inalcanzables",
                          "3 y 4 no tienen camino desde la fuente: nunca entran al deque")
        g, evs = escena("todo peso 1")
        self.animar_grafo(g, evs, "Caso borde: todas las aristas pesan 1",
                          "todo entra por atras: el deque se comporta como la cola de BFS normal")


class ComplejidadScene(BFS01Base):
    def construct(self):
        cab = self.titulo("Analisis de complejidad")
        self.play(FadeIn(cab, shift=DOWN * 0.3))

        def tarjeta(nombre, costo, detalle, color):
            caja = RoundedRectangle(corner_radius=0.2, width=5.8, height=3.0, color=color)
            txt = VGroup(T(nombre, 32, color=color), T(costo, 40),
                         *[T(d, 20, color=GRAY) for d in detalle]).arrange(DOWN, buff=0.18)
            return VGroup(caja, txt)

        bfs = tarjeta("BFS 0-1", "O(V + E)",
                      ["deque: push/pop en O(1)", "cada arista se relaja una vez", "cada nodo se procesa una vez"],
                      GREEN)
        dij = tarjeta("Dijkstra (heap)", "O((V + E) log V)",
                      ["heap: push/pop en O(log V)", "sirve para pesos >= 0 cualquiera",
                       "con pesos 0/1 paga log V de mas"], ORANGE)
        tarjetas = VGroup(bfs, dij).arrange(RIGHT, buff=0.6).shift(UP * 0.4)
        self.play(FadeIn(bfs, shift=UP * 0.3))
        self.wait(1.5)
        self.play(FadeIn(dij, shift=UP * 0.3))
        self.wait(1.5)

        espacio = T("Memoria: O(V + E)  (lista de adyacencia + dist + visited + deque)", 24)
        clave = T("Clave: con pesos 0/1 el deque queda ordenado por distancia sin necesidad de heap", 24,
                  color=YELLOW)
        VGroup(espacio, clave).arrange(DOWN, buff=0.25).next_to(tarjetas, DOWN, buff=0.5)
        self.play(Write(espacio), run_time=1.2)
        self.play(Write(clave), run_time=1.5)
        self.play(Indicate(bfs[1][1], color=GREEN))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])


class CreditosScene(BFS01Base):
    def construct(self):
        cab = self.titulo("Creditos")
        filas = VGroup(*[VGroup(T(rol, 26, color=GRAY), T(nombre, 30)).arrange(RIGHT, buff=0.5)
                         for rol, nombre in CREDITOS]).arrange(DOWN, buff=0.35)
        curso = T(CURSO, 22, color=GRAY).to_edge(DOWN, buff=0.6)
        nota = T("Animacion generada a partir de trace.jsonl de nuestra implementacion en C++", 20,
                 color=GRAY).next_to(curso, UP, buff=0.2)
        self.play(FadeIn(cab, shift=DOWN * 0.3))
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in filas], lag_ratio=0.3))
        self.play(FadeIn(nota), FadeIn(curso))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


class BFS01Video(BFS01Base):
    """Video completo: ejemplo -> casos borde -> complejidad -> creditos."""

    def construct(self):
        for cls in (EjemploScene, CasoBordeScene, ComplejidadScene, CreditosScene):
            cls.construct(self)
