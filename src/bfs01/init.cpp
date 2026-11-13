#include "bfs01/bfs01.h"

// Inicializa la fuente: dist = 0 y entra al deque por el frente, porque
// al arranque no hay nada mejor que explorar primero
void initBFS01(int source) {
    dist[source] = 0;
    dq.push_front(source);

    emit("init", "Nodo " + to_string(source) + " es la fuente, dist = 0", source);
}
