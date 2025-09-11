from ford_fulkerson import ford_fulkerson
from graph_generator import generate_random_graph, generate_manual_graph

global source
global sink
global graph
global edge_list
global capacity_map
global edge_capacities
global graph_flow_levels
global max_capacity_flow

def is_valid_flow(arr_edges):
    edges = {}
    for i in range(num_edges):
        if arr_edges[i] > 0:
            u, v, _ = edge_list[i]
            edges.setdefault(u, []).append(v)
            edges.setdefault(v, []).append(u)

    visited = set()

    def has_cycle(node, parent):
        visited.add(node)
        for neighbor in edges.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, node):
                    return True
            elif neighbor != parent:  # ignore the edge back to parent
                return True
        return False

    return not has_cycle(source, None)


def dfs_find_level_1(visited_nodes, node, arr):
    if node == sink:
        graph_flow_levels[1].append(arr[:])  # level 1 paths
        return

    for neighbor, cost, index in graph[node]:
        if neighbor not in visited_nodes:
            # set that this edge is used
            visited_nodes.add(neighbor)
            arr[index] = 1

            dfs_find_level_1(visited_nodes, neighbor, arr)

            # set that this edge is free to use for other paths
            visited_nodes.discard(neighbor)
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
                if valid and key not in hash_no_duplicates and is_valid_flow(arr_level):
                    graph_flow_levels[level].append(arr_level)
                    hash_no_duplicates.add(key)


if __name__ == '__main__':
    graph_flow_levels = [[], []]  # level 0 and level 1 initialized
    mode = input("Type 'r' for random graph or 'm' for manual: ").strip().lower()

    if mode == 'r':
        n = int(input("Number of nodes: "))
        num_edges = int(input("Number of edges: "))
        min_cap = int(input("Minimum capacity in graph: "))
        max_cap = int(input("Maximum capacity in graph: "))

        graph, residual_graph, capacity_map, edge_capacities, edge_list, num_edges = \
            generate_random_graph(n, num_edges, min_cap, max_cap)
    else:
        print("Number of edges:")
        num_edges = int(input())

        print("Start entering the edges in format -> node1 node2 capacity")
        graph, residual_graph, capacity_map, edge_capacities, edge_list = \
            generate_manual_graph(num_edges)

    source = int(input("Source (0 indexed): "))
    sink = int(input("Sink (0 indexed): "))

    max_capacity_flow = ford_fulkerson(residual_graph, capacity_map, source, sink)  # find max flow, which is the max flow level achieved in graph

    dfs_find_level_1({source}, source, [0 for _ in range(num_edges)])

    find_all_graph_flow_levels()

    print(graph_flow_levels)
