import heapq
import networkx as nx
from collections import defaultdict

# ── 1. Construcción del grafo y la tabla hash de perfiles ──
def construir_grafo(interacciones):
    """
    interacciones: lista de tuplas (usuario, contenido, puntuacion)
    Retorna: grafo dirigido ponderado + tabla hash de perfiles
    """
    G = nx.DiGraph()
    perfiles = defaultdict(dict)  # tabla hash: usuario -> {contenido: puntuacion}

    for usuario, contenido, puntuacion in interacciones:
        G.add_edge(usuario, contenido, weight=puntuacion)
        perfiles[usuario][contenido] = puntuacion

    return G, perfiles

# ── 2. Búsqueda de usuarios similares ──
def similitud_coseno(perfil_a, perfil_b):
    comunes = set(perfil_a.keys()) & set(perfil_b.keys())
    if not comunes:
        return 0.0
    numerador = sum(perfil_a[c] * perfil_b[c] for c in comunes)
    norma_a = sum(v**2 for v in perfil_a.values()) ** 0.5
    norma_b = sum(v**2 for v in perfil_b.values()) ** 0.5
    return numerador / (norma_a * norma_b) if norma_a * norma_b else 0.0

def usuarios_similares(perfiles, usuario_objetivo, top_k=3):
    scores = {}
    perfil_obj = perfiles.get(usuario_objetivo, {})
    for usuario, perfil in perfiles.items():
        if usuario != usuario_objetivo:
            scores[usuario] = similitud_coseno(perfil_obj, perfil)
    return sorted(scores, key=scores.get, reverse=True)[:top_k]

# ── 3. Recomendación con Dijkstra ──
def recomendar_dijkstra(G, perfiles, usuario, top_k=3):
    historial = set(perfiles.get(usuario, {}).keys())
    distancias = {c: 0.0 for c in historial}
    heap = [(0.0, c) for c in historial]
    heapq.heapify(heap)

    while heap:
        dist, nodo = heapq.heappop(heap)
        if dist > distancias.get(nodo, float('inf')):
            continue
        for vecino in G.successors(nodo):
            peso = G[nodo][vecino]['weight']
            distancia_inv = 1.0 / peso if peso > 0 else float('inf')
            nueva_dist = distancias[nodo] + distancia_inv
            if nueva_dist < distancias.get(vecino, float('inf')):
                distancias[vecino] = nueva_dist
                heapq.heappush(heap, (nueva_dist, vecino))

    candidatos = {c: d for c, d in distancias.items() if c not in historial}
    return sorted(candidatos, key=candidatos.get)[:top_k]

# ── 4. Demostración ──
if __name__ == '__main__':
    interacciones = [
        ("user_A", "Stranger Things",    5),
        ("user_A", "Black Mirror",       4),
        ("user_A", "Dark",               5),
        ("user_B", "Stranger Things",    5),
        ("user_B", "Dark",               4),
        ("user_B", "Squid Game",         5),
        ("user_C", "Black Mirror",       3),
        ("user_C", "Squid Game",         4),
        ("user_C", "Mindhunter",         5),
        ("user_D", "Dark",               3),
        ("user_D", "Mindhunter",         4),
        ("user_D", "Ozark",              5),
        ("user_E", "Mindhunter",         5),
        ("user_E", "Ozark",              5),
        ("user_E", "Stranger Things",    2),
        ("user_F", "Dark",               3),
    ]

    G, perfiles = construir_grafo(interacciones)

    G.add_edge("Stranger Things", "Dark",           weight=5)
    G.add_edge("Stranger Things", "Squid Game",     weight=4)
    G.add_edge("Stranger Things", "Mindhunter",     weight=3)
    G.add_edge("Dark",            "Stranger Things", weight=5)
    G.add_edge("Dark",            "Mindhunter",     weight=4)
    G.add_edge("Dark",            "Ozark",          weight=3)
    G.add_edge("Black Mirror",    "Mindhunter",     weight=4)
    G.add_edge("Black Mirror",    "Ozark",          weight=3)
    G.add_edge("Squid Game",      "Dark",           weight=4)
    G.add_edge("Squid Game",      "Mindhunter",     weight=3)
    G.add_edge("Mindhunter",      "Ozark",          weight=5)
    G.add_edge("Mindhunter",      "Dark",           weight=4)
    G.add_edge("Ozark",           "Mindhunter",     weight=5)
    G.add_edge("Ozark",           "Black Mirror",   weight=3)

    objetivo = "user_A"
    print(f"=== Recomendaciones para {objetivo} ===")
    print(f"Historial: {list(perfiles[objetivo].keys())}")

    similares = usuarios_similares(perfiles, objetivo)
    print(f"Usuarios más similares: {similares}")

    recomendaciones = recomendar_dijkstra(G, perfiles, objetivo)
    print(f"Contenido recomendado:  {recomendaciones}")
