from graph import Graph, Edge

if __name__ == "__main__":
    filename = "resources/Graph_A-H.csv"
    g = Graph()
    g.read_graph_from_adjacency_matrix_file(filename)
    print(g)

    (edgelist, path, cost) = g.uniform_cost_search("A", "G")
    print(f"{path=} ({cost=})")
    (edgelist, path, cost) = g.get_longest_shortest_path_in_graph()
    print(path)
    print(cost)
    print(g.get_all_paths("A"))
    print(g.get_all_paths("H"))
