def dfs(node, sink, graph, capacity_map, visited, path):
    if node == sink:
        return True

    visited.add(node)

    for neighbor, _ in graph[node]:
        if neighbor not in visited and capacity_map.get((node, neighbor), 0) > 0:
            path.append(neighbor)
            if dfs(neighbor, sink, graph, capacity_map, visited, path):
                return True
            path.pop()

    return False


def ford_fulkerson(graph, capacity_map, source, sink):
    max_flow = 0

    while True:
        visited = set()
        path = [source]

        if not dfs(source, sink, graph, capacity_map, visited, path):
            break

        path_flow = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            path_flow = min(path_flow, capacity_map[(u, v)])

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            capacity_map[(u, v)] -= path_flow
            capacity_map[(v, u)] = capacity_map.get((v, u), 0) + path_flow

        max_flow += path_flow

    return max_flow
