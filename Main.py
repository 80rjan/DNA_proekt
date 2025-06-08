from ford_fulkerson import ford_fulkerson

global source
global sink
global graph
global capacity_map
global edge_capacities
global graph_flow_levels
global max_capacity_flow


def dfs_find_level_1(visited_edge, node, arr):
    if node == sink:
        graph_flow_levels[1].append(arr[:])  # level 1 paths
        return

    for neighbor, cost, index in graph[node]:
        if index not in visited_edge:
            # set that this edge is used
            visited_edge.add(index)
            arr[index] = 1

            dfs_find_level_1(visited_edge, neighbor, arr)

            # set that this edge is free to use for other paths
            visited_edge.discard(index)
            arr[index] = 0


def find_all_graph_flow_levels():
    for level in range(2, max_capacity_flow + 1):
        graph_flow_levels.append([])
        arr_first_sum = graph_flow_levels[level // 2]
        arr_second_sum = graph_flow_levels[level - level // 2]
        hash_no_duplicates = set()

        for level_first_sum in arr_first_sum:
            for level_second_sum in arr_second_sum:
                valid = True
                arr_level = []
                for i in range(num_edges):
                    total = level_first_sum[i] + level_second_sum[i]
                    if total > edge_capacities[i]:
                        valid = False
                        break
                    arr_level.append(total)

                key = tuple(arr_level)
                if valid and key not in hash_no_duplicates:
                    graph_flow_levels[level].append(arr_level)
                    hash_no_duplicates.add(key)


if __name__ == '__main__':
    print("Vnesi broj na rebra")
    num_edges = int(input())

    source = 0
    sink = 0

    graph = {}  # key: u, value: (v, capacity, edge_index)
    residual_graph = {}  # residual graph for ford fulkerson
    capacity_map = {}  # key: (u, v), value: capacity. Used for ford fulkerson
    edge_capacities = []  # capacities of all edges. Used for finding graph flow levels

    graph_flow_levels = [[], []]  # level 0 and level 1 initialized

    print("Vnesuvaj rebra")

    for i in range(num_edges):
        a, b, c = list(map(int, input().split()))

        sink = max(sink, a, b)  # find the sink (could be entered in input)

        if a not in graph:
            graph[a] = []
            residual_graph[a] = []
        if b not in graph:
            graph[b] = []
            residual_graph[b] = []

        graph[a].append((b, c, i))
        residual_graph[a].append((b, c))
        residual_graph[b].append((a, 0))
        capacity_map[(a, b)] = c
        edge_capacities.append(c)

    max_capacity_flow = ford_fulkerson(residual_graph, capacity_map, source, sink)  # find max flow, which is the max flow level achieved in graph

    dfs_find_level_1(set(), 0, [0 for _ in range(num_edges)])

    find_all_graph_flow_levels()

    print(graph_flow_levels)
