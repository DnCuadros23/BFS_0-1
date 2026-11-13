#include "bfs01/bfs01.h"

void bfs01(int source) {
    initBFS01(source);

    while (!dq.empty()) {
        int u = dq.front();
        dq.pop_front();

        if (visited[u]) {
            emit("skip", "Nodo " + to_string(u) + " ya fue procesado, se descarta", u);
            continue;
        }
        visited[u] = true;
        emit("pop", "Sale el nodo " + to_string(u) + " con dist = " + to_string(dist[u]), u);

        for (auto& [v, w] : adj[u]) {
            long long nd = dist[u] + w;
            string arista = to_string(u) + "->" + to_string(v) + " (peso " + to_string(w) + ")";

            if (dist[v] != -1 && nd >= dist[v]) {
                emit("keep", "Arista " + arista + ": dist[" + to_string(v) + "] = " +
                     to_string(dist[v]) + " no mejora", u, u, v, w);
                continue;
            }

            dist[v] = nd;
            if (w == 0) {
                dq.push_front(v);
                emit("relax", "Arista " + arista + ": dist[" + to_string(v) + "] = " +
                     to_string(nd) + ", entra por el frente", v, u, v, w, "front");
            } else {
                dq.push_back(v);
                emit("relax", "Arista " + arista + ": dist[" + to_string(v) + "] = " +
                     to_string(nd) + ", entra por atras", v, u, v, w, "back");
            }
        }
    }

    emit("done", "Deque vacio: distancias finales calculadas");
}
