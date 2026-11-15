#ifndef DEMO_CASES_H
#define DEMO_CASES_H

// Grafo de ejemplo ilustrativo: tiene aristas de peso 0 y 1, un nodo que entra
// dos veces al deque (genera "skip") y aristas que no mejoran ("keep").
void demoEjemplo();

// Caso borde: nodos inalcanzables desde la fuente (quedan con dist = -1 / infinito).
void demoInalcanzable();

// Caso borde: todas las aristas pesan 1 (BFS 0-1 se comporta como BFS normal).
void demoTodoPeso1();

#endif
