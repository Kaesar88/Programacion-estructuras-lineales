import heapq

# ── 1. Dijkstra para distancias mínimas desde el origen ──
def dijkstra(grafo, origen):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    heap = [(0, origen)]

    while heap:
        dist_actual, nodo_actual = heapq.heappop(heap)
        if dist_actual > distancias[nodo_actual]:
            continue
        for vecino, peso in grafo[nodo_actual].items():
            nueva_dist = distancias[nodo_actual] + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                heapq.heappush(heap, (nueva_dist, vecino))

    return distancias

# ── 2. Priorización de entregas por urgencia y distancia ──
def priorizar_entregas(grafo, origen, entregas):
    distancias = dijkstra(grafo, origen)
    cola = []

    for destino, urgencia in entregas:
        dist = distancias[destino]
        if dist > 0:
            puntuacion = urgencia / dist
        else:
            puntuacion = float('inf')
        heapq.heappush(cola, (-puntuacion, destino))

    orden = []
    while cola:
        _, destino = heapq.heappop(cola)
        orden.append(destino)

    return orden, distancias

# ── 3. Demostración ──
if __name__ == '__main__':
    grafo = {
        'Almacen':  {'Punto_A': 5,  'Punto_B': 10, 'Punto_D': 20},
        'Punto_A':  {'Almacen': 5,  'Punto_B': 3,  'Punto_C': 15},
        'Punto_B':  {'Almacen': 10, 'Punto_A': 3,  'Punto_C': 7,  'Punto_D': 6},
        'Punto_C':  {'Punto_A': 15, 'Punto_B': 7,  'Punto_D': 2},
        'Punto_D':  {'Almacen': 20, 'Punto_B': 6,  'Punto_C': 2},
    }

    # (destino, nivel_urgencia): urgencia de 1 (baja) a 5 (alta)
    entregas = [
        ('Punto_A', 3),
        ('Punto_B', 5),
        ('Punto_C', 2),
    ]

    origen = 'Almacen'
    orden, distancias = priorizar_entregas(grafo, origen, entregas)

    print(f"=== Optimización de rutas para {origen} ===")
    print(f"\nDistancias mínimas desde {origen}:")
    for nodo, dist in distancias.items():
        print(f"  {nodo}: {dist}")

    print(f"\nOrden óptimo de entregas (urgencia/distancia):")
    for i, destino in enumerate(orden, 1):
        dist = distancias[destino]
        urgencia = dict(entregas)[destino]
        print(f"  {i}. {destino} — distancia: {dist}, urgencia: {urgencia}, "
              f"puntuación: {urgencia/dist:.3f}")
