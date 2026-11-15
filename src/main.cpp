#include "demo_cases.h"
#include <iostream>

using namespace std;

// Corre el algoritmo real sobre todos los grafos de demo.
// Cada buildGraph() agrega un evento "graph" a trace.jsonl, que Manim usa para
// separar las escenas (ver animation/render_bfs01.py).
int main() {
    cout << "=== BFS 0-1: demo ===" << endl;
    demoEjemplo();
    demoInalcanzable();
    demoTodoPeso1();
    cout << "Listo: trace.jsonl generado" << endl;
    return 0;
}
