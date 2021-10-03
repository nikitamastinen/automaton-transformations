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
        for edge in edges:
            e = Edge(edge[0], edge[1], edge[2])
            self.add_edge(e)

    def reindex_vertices(self):
        self.add_empty_keys()
        reindex_map: Dict[str] = {}
        index: int = 0
        for key in self.graph.keys():
            reindex_map[key] = str(index)
            index += 1

        indexed_graph: Dict[str, List[Edge]] = {}
        for key in self.graph.keys():
            for e in self.graph[key]:
                if reindex_map[e.start] in indexed_graph:
                    indexed_graph[reindex_map[e.start]].append(
                        Edge(
                            reindex_map[e.start],
                            reindex_map[e.end],
                            e.value,
                        )
                    )
                else:
                    indexed_graph[reindex_map[e.start]] = [
                        Edge(
                            reindex_map[e.start],
                            reindex_map[e.end],
                            e.value,
                        )
                    ]
        self.graph = indexed_graph
        self.start = reindex_map[self.start]
        self.terminals = {reindex_map[i] for i in self.terminals}

    def add_empty_keys(self) -> None:
        for i in self.terminals:
            if i not in self.graph:
                self.graph[i] = []
        if self.start not in self.graph:
            self.graph[self.start] = []
        old_keys: List = deepcopy([*self.graph.keys()])
        for key in old_keys:
            for e in self.graph[key]:
                if e.start not in self.graph:
                    self.graph[e.start] = []
                if e.end not in self.graph:
                    self.graph[e.end] = []

    def add_edge(self, e: Edge):
        if e.start in self.graph.keys():
            if e not in self.graph[e.start]:
                self.graph[e.start].append(e)
        else:
            self.graph[e.start] = [e]

    def print(self):
        print("head:")
        print(self.start)
        print("edges:")
        for key in self.graph:
            for e in self.graph[key]:
                print(e.start, e.end, e.value)
        print("terminals:")
        print(*self.terminals)

    def dict(self):
        answer: Dict = {'head': self.start, 'edges': [], 'terminals': []}
        for key in self.graph:
            for e in self.graph[key]:
                answer['edges'].append((
                    e.start,
                    e.end,
                    e.value,
                ))
        answer['edges'].sort()
        answer['terminals'] = [i for i in self.terminals]
        answer['terminals'].sort()
        return answer
