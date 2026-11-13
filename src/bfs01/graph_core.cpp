#include "../../include/bfs01/bfs01.h"
#include <fstream>
#include <sstream>

using namespace std;

vector<vector<pair<int, int>>> adj;
vector<long long> dist;
vector<bool> visited;
deque<int> dq;

void buildGraph(int n, vector<tuple<int, int, int>> edges) {
    adj.assign(n, {});
    dist.assign(n, -1);
    visited.assign(n, false);
    dq.clear();

    for (auto& [u, v, w] : edges) {
        adj[u].push_back({v, w});
    }
}

void emit(const string& event, const string& note, int currentNode) {
    static ofstream trace_file("trace.jsonl");

    // Snapshot de todos los nodos (dist + visited)
    stringstream nodes;
    nodes << "[";
    for (int i = 0; i < (int)dist.size(); i++) {
        if (i > 0) nodes << ",";
        nodes << "{\"id\":" << i << ",\"dist\":" << dist[i]
              << ",\"visited\":" << (visited[i] ? "true" : "false") << "}";
    }
    nodes << "]";

    // Contenido actual del deque
    stringstream deq;
    deq << "[";
    for (int i = 0; i < (int)dq.size(); i++) {
        if (i > 0) deq << ",";
        deq << dq[i];
    }
    deq << "]";

    // Armar la linea completa en JSON
    string json_line = "{";
    json_line += "\"event\":\"" + event + "\",";
    json_line += "\"note\":\"" + note + "\",";
    json_line += "\"current_node\":" + to_string(currentNode) + ",";
    json_line += "\"nodes\":" + nodes.str() + ",";
    json_line += "\"deque\":" + deq.str();
    json_line += "}";

    // Escribir la linea en el archivo (una linea por evento)
    trace_file << json_line << "\n";
    trace_file.flush();
}
