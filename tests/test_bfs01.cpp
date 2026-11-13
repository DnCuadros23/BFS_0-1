#include "bfs01/bfs01.h"
#include <iostream>

using namespace std;

bool check(const vector<long long>& expected) {
    for (int i = 0; i < (int)expected.size(); i++) {
        if (dist[i] != expected[i]) {
            cout << "  FALLA en nodo " << i << ": esperado " << expected[i]
                 << ", obtenido " << dist[i] << endl;
            return false;
        }
    }
    return true;
}

int main() {
    cout << "=== Test bfs01 ===" << endl;
    int fallas = 0;

    buildGraph(6, {
        {0, 1, 1}, {0, 2, 0}, {2, 1, 0}, {1, 3, 1},
        {2, 4, 1}, {4, 3, 0}, {3, 5, 1}, {4, 5, 1},
    }, "ejemplo");
    bfs01(0);
    cout << "Ejemplo: " << (check({0, 0, 0, 1, 1, 2}) ? "OK" : "FALLA") << endl;
    fallas += !check({0, 0, 0, 1, 1, 2});

    buildGraph(4, {{0, 1, 1}, {1, 0, 0}, {2, 3, 0}}, "inalcanzable");
    bfs01(0);
    cout << "Inalcanzable: " << (check({0, 1, -1, -1}) ? "OK" : "FALLA") << endl;
    fallas += !check({0, 1, -1, -1});

    buildGraph(1, {}, "un nodo");
    bfs01(0);
    cout << "Un nodo: " << (check({0}) ? "OK" : "FALLA") << endl;
    fallas += !check({0});

    buildGraph(4, {{0, 1, 1}, {1, 2, 1}, {2, 3, 1}, {0, 3, 1}}, "todo peso 1");
    bfs01(0);
    cout << "Todo peso 1: " << (check({0, 1, 2, 1}) ? "OK" : "FALLA") << endl;
    fallas += !check({0, 1, 2, 1});

    cout << (fallas == 0 ? "Todo correcto" : "Hay fallas") << ", revisa trace.jsonl" << endl;
    return fallas;
}
