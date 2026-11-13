#ifndef BFS01_H
#define BFS01_H

#include <vector>
#include <deque>
#include <string>
#include <tuple>

using namespace std;

// Grafo dirigido: adj[u] = lista de (vecino, peso)
extern vector<vector<pair<int, int>>> adj;
extern vector<long long> dist;    // -1 = todavia no alcanzado
extern vector<bool> visited;      // se marca al sacar el nodo del deque
extern deque<int> dq;

// Arma el grafo a partir de las aristas (u, v, peso) y emite el evento "graph"
void buildGraph(int n, vector<tuple<int, int, int>> edges, const string& name = "grafo");

// Guarda un evento en trace.jsonl para que Manim lo anime despues
// event: que paso (init, pop, relax, keep, skip, done)
// note: texto para el subtitulo
// currentNode: nodo resaltado en la animacion (-1 si ninguno)
// edgeU, edgeV, weight: arista que se esta revisando (-1 si ninguna)
// side: "front" o "back" si el vecino entro al deque, "" si no
void emit(const string& event, const string& note, int currentNode = -1,
          int edgeU = -1, int edgeV = -1, int weight = -1, const string& side = "");

// Inicializa dist/visited/dq para la fuente (Persona 1)
void initBFS01(int source);

// Llama a initBFS01 y corre el bucle principal (Persona 2)
void bfs01(int source);

#endif
