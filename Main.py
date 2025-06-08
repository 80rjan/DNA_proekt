global source
global sink
global graph
global edge_capacities
global graph_flow_levels
global max_capacity_flow


def dfs(visited_edge, node, arr):
    if node == sink:
        graph_flow_levels[1].append(arr[:])  # level 1 paths
        return

    for neighbor, cost, index in graph[node]:
        edge = (source, neighbor)
        if not visited_edge.get(edge, False):
            # set that this edge is used
            visited_edge[edge] = True
            arr[index] = 1

            dfs(visited_edge, neighbor, arr)

            # set that this edge is free to use for other paths
            visited_edge[edge] = False
            arr[index] = 0


def find_all_graph_flow_levels():
    for level in range(2, max_capacity_flow + 1):
        graph_flow_levels.append([])
        arr_first_sum = graph_flow_levels[level // 2]
        arr_second_sum = graph_flow_levels[level - level // 2]

        for l1 in arr_first_sum:
            for l2 in arr_second_sum:
                arr_level = []
                for i, (el1, el2) in enumerate(zip(l1, l2)):
                    if el1 + el2 > edge_capacities[i]:
                        break
                    arr_level.append(el1 + el2)
                if len(arr_level) == num_edges:
                    graph_flow_levels[level].append(arr_level)


if __name__ == '__main__':
    print("Vnesi broj na rebra")
    num_edges = int(input())

    source = 0
    sink = 0

    graph = {}  # adjacency list graph (u, v, cost, edge_index)
    edge_capacities = []  # capacities of all edges

    graph_flow_levels = [[], []]

    max_capacity_flow = 0  # find max capacity flow, which is the max flow level achieved in graph

    print("Vnesuvaj rebra")

    source_total_capacity = 0
    for i in range(num_edges):
        a, b, c = list(map(int, input().split()))

        if a == 0:
            source_total_capacity += c
        else:
            max_capacity_flow = max(max_capacity_flow, c)

        sink = max(sink, a, b)  # find the sink (could be entered in input)

        if a not in graph:
            graph[a] = []
        graph[a].append((b, c, i))
        edge_capacities.append(c)

    max_capacity_flow = min(max_capacity_flow, source_total_capacity)  # optimize if source edges are bottleneck

    dfs({}, 0, [0 for _ in range(num_edges)])

    find_all_graph_flow_levels()

    print(graph_flow_levels)
