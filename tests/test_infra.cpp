#include "bfs01/bfs01.h"
#include <iostream>

using namespace std;

// Prueba rapida de buildGraph() y emit(), simulando a mano un par de pasos
// del algoritmo (todavia no existen initBFS01()/bfs01())
int main() {
    cout << "=== Test infra: buildGraph + emit ===" << endl;

    buildGraph(4, {
        {0, 1, 0},
        {0, 2, 1},
        {1, 2, 0},
        {2, 3, 1},
    });
    emit("build", "Grafo construido: 4 nodos", -1);

    // Simula initBFS01(0): la fuente arranca en dist 0
    dist[0] = 0;
    visited[0] = true;
    dq.push_front(0);
    emit("init", "Nodo 0 es la fuente", 0);

    // Simula un paso de bfs01(): relaja la arista 0->1 (peso 0)
    dq.pop_front();
    dist[1] = 0;
    dq.push_front(1);
    emit("relax", "Relajando arista 0->1 (peso 0)", 1);

    cout << "Listo, revisa trace.jsonl" << endl;
    return 0;
}
