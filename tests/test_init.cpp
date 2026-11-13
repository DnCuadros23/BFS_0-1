#include "bfs01/bfs01.h"
#include <iostream>

using namespace std;

// Prueba rapida de initBFS01(), sin depender de bfs01() (todavia no existe)
int main() {
    cout << "=== Test init: initBFS01 ===" << endl;

    buildGraph(3, {
        {0, 1, 0},
        {1, 2, 1},
    });

    initBFS01(0);

    cout << "dist[0] = " << dist[0] << endl;
    cout << "deque.front() = " << dq.front() << endl;
    cout << "Listo, revisa trace.jsonl" << endl;
    return 0;
}
