from graph import Graph, Edge

if __name__ == "__main__":
    filename = "resources/Graph_A-H.csv"
    g = Graph()
    g.read_graph_from_adjacency_matrix_file(filename)
    print(g)