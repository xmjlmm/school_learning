# import heapq
# import math
# graph = {
#     "A": {"B": 5, "C": 1},
#     "B": {"A": 5, "C": 2, "D": 1},
#     "C": {"A": 1, "B": 2, "D": 4, "E": 8},
#     "D": {"B": 1, "C": 4, "E": 3, "F": 6},
#     "E": {"C": 8, "D": 3},
#     "F": {"D": 6}
# }

# def init_distance(graph, s):
#     d = {}
#     d[s] = 0
#     for j in graph.keys():
#         if j not in d:
#             d[j] = math.inf
#     return d

# def dijkstra(graph, s):
#     pqueue = []
#     heapq.heappush(pqueue, (0, s))
#     seen = set()
#     parent = {s: None}
#     distance = init_distance(graph, s)

#     while (len(pqueue) > 0):
#         pair = heapq.heappop(pqueue)
#         dist, vertex = pair[0], pair[1]
#         seen.add(vertex)

#         nodes = graph[vertex].keys()
#         for w in nodes:
#             if w not in seen:
#                 if dist + graph[vertex][w] < distance[w]:
#                     heapq.heappush(pqueue, (dist + graph[vertex][w], w))
#                     parent[w] = vertex
#                     distance[w] = dist + graph[vertex][w]
#     return parent, distance

# def main():
#     parent, distance = dijkstra(graph, "A")
#     print(parent)
#     print(distance)

# if __name__ == "__main__":
#     main()



import heapq
import math
graph = {
    "A": {"B": 5, "C": 1},
    "B": {"A": 5, "C": 2, "D": 1},
    "C": {"A": 1, "B": 2, "D": 4, "E": 8},
    "D": {"B": 1, "C": 4, "E": 3, "F": 6},
    "E": {"C": 8, "D": 3},
    "F": {"D": 6}
}

def init_distance(graph, s):
    d = {}
    d[s] = 0
    for j in graph.keys():
        if j not in d:
            d[j] = math.inf
    return d

def dijkstra(graph, s):
    pqueue = []
    heapq.heappush(pqueue, (0, s))
    seen = set()
    parent = {s: None}
    distance = init_distance(graph, s)

    while (len(pqueue) > 0):
        pair = heapq.heappop(pqueue)
        dist, vertex = pair[0], pair[1]
        seen.add(vertex)

        nodes = graph[vertex].keys()
        for w in nodes:
            if w not in seen:
                if dist + graph[vertex][w] < distance[w]:
                    heapq.heappush(pqueue, (dist + graph[vertex][w], w))
                    parent[w] = vertex
                    distance[w] = dist + graph[vertex][w]
    return parent, distance

def main():
    parent, distance = dijkstra(graph, "A")
    print(parent)
    print(distance)

if __name__ == "__main__":
    main()