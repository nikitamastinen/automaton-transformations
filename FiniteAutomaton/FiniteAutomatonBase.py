from typing import List, Dict, Set, Tuple
from copy import deepcopy
from FiniteAutomaton.Edge import Edge


class FiniteAutomatonBase:
    def __init__(
            self,
            edges: List[Tuple[str, str, str]],
            terminals: Set[str],
            alphabet: List[str],
            start: str,
    ):
        self.alphabet = deepcopy(alphabet)
        self.start = start
        self.graph: Dict[str, List[Edge]] = dict()
        self.terminals: Set[str] = deepcopy(terminals)
        for start, finish, value in edges:
            edge = Edge(start, finish, value)
            self.add_edge(edge)

    def reindex_vertices(self):
        self.add_empty_keys()
        reindex_map: Dict[str] = {}
        index: int = 0
        for key in self.graph.keys():
            reindex_map[key] = str(index)
            index += 1

        indexed_graph: Dict[str, List[Edge]] = {}
        for key in self.graph.keys():
            for edge in self.graph[key]:
                if reindex_map[edge.start] in indexed_graph:
                    indexed_graph[reindex_map[edge.start]].append(
                        Edge(
                            reindex_map[edge.start],
                            reindex_map[edge.end],
                            edge.value,
                        )
                    )
                else:
                    indexed_graph[reindex_map[edge.start]] = [
                        Edge(
                            reindex_map[edge.start],
                            reindex_map[edge.end],
                            edge.value,
                        )
                    ]
        self.graph = indexed_graph
        self.start = reindex_map[self.start]
        self.terminals = {reindex_map[vertex] for vertex in self.terminals}

    def add_empty_keys(self) -> None:
        for vertex in self.terminals:
            if vertex not in self.graph:
                self.graph[vertex] = []
        if self.start not in self.graph:
            self.graph[self.start] = []
        old_keys: List = deepcopy([*self.graph.keys()])
        for key in old_keys:
            for edge in self.graph[key]:
                if edge.start not in self.graph:
                    self.graph[edge.start] = []
                if edge.end not in self.graph:
                    self.graph[edge.end] = []

    def add_edge(self, edge: Edge):
        if edge.start in self.graph.keys():
            if edge not in self.graph[edge.start]:
                self.graph[edge.start].append(edge)
        else:
            self.graph[edge.start] = [edge]

    def print(self):
        print("head:")
        print(self.start)
        print("edges:")
        for key in self.graph:
            for edge in self.graph[key]:
                print(edge.start, edge.end, edge.value)
        print("terminals:")
        print(*self.terminals)

    def dump(self):
        converted: Dict = {'head': self.start, 'edges': [], 'terminals': []}
        for key in self.graph:
            for edge in self.graph[key]:
                converted['edges'].append((
                    edge.start,
                    edge.end,
                    edge.value,
                ))
        converted['edges'].sort()
        converted['terminals'] = [vertex for vertex in self.terminals]
        converted['terminals'].sort()
        return converted
