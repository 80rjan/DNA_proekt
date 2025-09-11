import random

def generate_random_graph(num_nodes: int,
                          num_edges: int,
                          min_cap: int,
                          max_cap: int):
    max_possible_edges = num_nodes * (num_nodes - 1) // 2
    if num_edges > max_possible_edges:
        print(f"Warning: requested {num_edges} edges, "
              f"but only {max_possible_edges} unique edges possible. "
              f"Generating {max_possible_edges} edges instead.")
        num_edges = max_possible_edges

    graph = {}  # key: u, value: (v, capacity, edge_index)
    residual_graph = {}  # residual graph for ford fulkerson
    capacity_map = {}  # key: (u, v), value: capacity. Used for ford fulkerson
    edge_capacities = []  # capacities of all edges. Used for finding graph flow levels
    edge_list = []  # edge information based on its index. Used for is_valid_flow for finding cycles in graph
    used_pairs = set()  # store unordered pairs to avoid duplicates

    while len(edge_list) < num_edges:
        # pick two different nodes
        u, v = random.sample(range(num_nodes), 2)

        pair = (min(u, v), max(u, v))
        if pair in used_pairs:
            continue  # skip if we already used this pair
        used_pairs.add(pair)

        c = random.randint(min_cap, max_cap)

        graph.setdefault(u, []).append((v, c, len(edge_list)))
        graph.setdefault(v, []).append((u, c, len(edge_list)))

        residual_graph.setdefault(u, []).append((v, c))
        residual_graph.setdefault(v, []).append((u, 0))

        capacity_map[(u, v)] = c
        edge_capacities.append(c)
        print(f'{len(edge_list)}: {u} <-> {v}     {c}')
        edge_list.append((u, v, c))

    return graph, residual_graph, capacity_map, edge_capacities, edge_list, num_edges

def generate_manual_graph(num_edges: int):
    graph = {}  # key: u, value: (v, capacity, edge_index)
    residual_graph = {}  # residual graph for ford fulkerson
    capacity_map = {}  # key: (u, v), value: capacity. Used for ford fulkerson
    edge_capacities = []  # capacities of all edges. Used for finding graph flow levels
    edge_list = []  # edge information based on its index. Used for is_valid_flow for finding cycles in graph

    for i in range(num_edges):
        a, b, c = map(int, input().split())

        graph.setdefault(a, []).append((b, c, i))
        graph.setdefault(b, []).append((a, c, i))
        residual_graph.setdefault(a, []).append((b, c))
        residual_graph.setdefault(b, []).append((a, 0))

        capacity_map[(a, b)] = c
        edge_capacities.append(c)
        edge_list.append((a, b, c))

    return graph, residual_graph, capacity_map, edge_capacities, edge_list