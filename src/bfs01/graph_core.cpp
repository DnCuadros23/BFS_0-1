#include "bfs01/bfs01.h"
#include <fstream>
#include <sstream>

using namespace std;

vector<vector<pair<int, int>>> adj;
vector<long long> dist;
vector<bool> visited;
deque<int> dq;

static ofstream& traceFile() {
    static ofstream trace_file("trace.jsonl");
    return trace_file;
}

static string escapeJson(const string& s) {
    string out;
    for (char c : s) {
        if (c == '"' || c == '\\') out += '\\';
        out += c;
    }
    return out;
}

void buildGraph(int n, vector<tuple<int, int, int>> edges, const string& name) {
    adj.assign(n, {});
    dist.assign(n, -1);
    visited.assign(n, false);
    dq.clear();

    for (auto& [u, v, w] : edges) {
        adj[u].push_back({v, w});
    }

    stringstream line;
    line << "{\"event\":\"graph\",\"name\":\"" << escapeJson(name) << "\",\"n\":" << n << ",\"edges\":[";
    for (int i = 0; i < (int)edges.size(); i++) {
        auto& [u, v, w] = edges[i];
        if (i > 0) line << ",";
        line << "{\"u\":" << u << ",\"v\":" << v << ",\"w\":" << w << "}";
    }
    line << "]}";
    traceFile() << line.str() << "\n";
    traceFile().flush();
}

void emit(const string& event, const string& note, int currentNode,
          int edgeU, int edgeV, int weight, const string& side) {
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
    json_line += "\"event\":\"" + escapeJson(event) + "\",";
    json_line += "\"note\":\"" + escapeJson(note) + "\",";
    json_line += "\"current_node\":" + to_string(currentNode) + ",";
    json_line += "\"edge\":";
    if (edgeU == -1) json_line += "null,";
    else json_line += "{\"u\":" + to_string(edgeU) + ",\"v\":" + to_string(edgeV) + ",\"w\":" + to_string(weight) + "},";
    json_line += "\"side\":\"" + side + "\",";
    json_line += "\"nodes\":" + nodes.str() + ",";
    json_line += "\"deque\":" + deq.str();
    json_line += "}";

    // Escribir la linea en el archivo (una linea por evento)
    traceFile() << json_line << "\n";
    traceFile().flush();
}
