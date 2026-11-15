#include "demo_cases.h"
#include "bfs01/bfs01.h"
#include <iostream>

using namespace std;

static void imprimirDistancias(const string& nombre) {
    cout << "[" << nombre << "] distancias:";
    for (int i = 0; i < (int)dist.size(); i++) {
        cout << " " << i << "=";
        if (dist[i] == -1) cout << "inf";
        else cout << dist[i];
    }
    cout << endl;
}

// 6 nodos. La ruta "barata" 0 -0-> 2 -0-> 1 le gana a la arista directa 0 -1-> 1,
// asi que el nodo 1 entra dos veces al deque (la segunda vez se descarta con "skip").
// 4 -0-> 3 no mejora dist[3] y 3 -1-> 5 tampoco mejora dist[5] ("keep").
void demoEjemplo() {
    buildGraph(6, {
        {0, 1, 1}, {0, 2, 0}, {2, 1, 0}, {1, 3, 1},
        {2, 4, 1}, {4, 3, 0}, {3, 5, 1}, {4, 5, 1},
    }, "ejemplo");
    bfs01(0);
    imprimirDistancias("ejemplo");  // esperado: 0 0 0 1 1 2
}

// Los nodos 3 y 4 forman una componente aparte: nunca entran al deque.
void demoInalcanzable() {
    buildGraph(5, {
        {0, 1, 1}, {1, 2, 0}, {2, 0, 1}, {3, 4, 0}, {4, 2, 1},
    }, "inalcanzable");
    bfs01(0);
    imprimirDistancias("inalcanzable");  // esperado: 0 1 1 inf inf
}

// Sin aristas de peso 0 todo entra por atras: el deque actua como una cola FIFO.
void demoTodoPeso1() {
    buildGraph(5, {
        {0, 1, 1}, {0, 2, 1}, {1, 3, 1}, {2, 3, 1}, {3, 4, 1},
    }, "todo peso 1");
    bfs01(0);
    imprimirDistancias("todo peso 1");  // esperado: 0 1 1 2 3
}
