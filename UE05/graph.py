from dataclasses import dataclass
from typing import TypeVar, Generic, List, Tuple, Optional
from queue import PriorityQueue

V = TypeVar('V')  # Typ der Knoten im Graphen


@dataclass
class Edge:
    u: int
    v: int
    weight: float

    def __repr__(self):
        return f"{self.u} --{self.weight}-> {self.v}"


class Graph(Generic[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices
        self._edges: List[List[Edge]] = [[] for _ in vertices]

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return sum(len(edges) for edges in self._edges) // 2  # Each edge is stored twice

    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])
        return len(self._vertices) - 1

    def add_edge(self, edge: Edge) -> None:
        if edge not in self._edges[edge.u]:
            self._edges[edge.u].append(edge)
        if edge not in self._edges[edge.v]:
            self._edges[edge.v].append(Edge(edge.v, edge.u, edge.weight))

    def add_edge_by_indices(self, u: int, v: int, w=1) -> Edge:
        edge = Edge(u, v, w)
        self.add_edge(edge)
        return edge

    def add_edge_by_vertices(self, first: V, second: V, w: float = 1) -> Edge:
        u, v = self.index_of(first), self.index_of(second)
        return self.add_edge_by_indices(u, v, w)

    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    def neighbors_for_index_with_weights(self, index: int) -> List[Tuple[V, float]]:
        return [(self.vertex_at(edge.v), edge.weight) for edge in self._edges[index]]

    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    def edge_list_to_string(self, edge_list: List[Edge], showWeights: bool = False) -> str:
        if showWeights:
            return "->".join(f"{self.vertex_at(e.u)}-{e.weight}->{self.vertex_at(e.v)}" for e in edge_list)
        return "->".join(f"{self.vertex_at(e.u)}" for e in edge_list) + f"->{self.vertex_at(edge_list[-1].v)}"

    def set_adjacency_matrix(self, lines: List[str]) -> None:
        lines = [line.strip() for line in lines if line.strip()]
        headers = lines[0].split(";")[1:]
        if len(headers) != len(set(headers)):
            raise RuntimeError("Duplicated Nodes in Adjacency Matrix")

        self._vertices = headers
        self._edges = [[] for _ in headers]
        for i, line in enumerate(lines[1:]):
            parts = line.split(";")
            if parts[0] != headers[i]:
                raise RuntimeError("Row headers do not match column headers")
            if len(parts[1:]) != len(headers):
                raise RuntimeError("Row length does not match column count")

            for j, weight in enumerate(parts[1:]):
                weight = weight.strip()
                if weight:
                    self.add_edge_by_indices(i, j, float(weight))

    def read_graph_from_adjacency_matrix_file(self, filename: str) -> None:
        with open(filename, 'r') as file:
            self.set_adjacency_matrix(file.readlines())

    def __str__(self) -> str:
        return "\n".join(f"{v} -> {self.neighbors_for_index_with_weights(i)}" for i, v in enumerate(self._vertices))

    def uniform_cost_search(self, start: V, goal: V) -> Tuple[List[Edge], str, float]:
        start_index, goal_index = self.index_of(start), self.index_of(goal)
        return self.uniform_cost_search_by_index(start_index, goal_index)

    def uniform_cost_search_by_index(self, start_index: int, goal_index: int) -> Tuple[List[Edge], str, float]:
        pq = PriorityQueue()
        pq.put((0, start_index, []))
        visited = set()

        while not pq.empty():
            cost, current, path = pq.get()
            if current in visited:
                continue
            visited.add(current)

            if current == goal_index:
                path_str = self.edge_list_to_string(path, showWeights=True)
                return path, path_str, cost

            for edge in self.edges_for_index(current):
                if edge.v not in visited:
                    pq.put((cost + edge.weight, edge.v, path + [edge]))

        return [], "No Path", float('inf')
