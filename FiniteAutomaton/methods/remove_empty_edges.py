from typing import Set

from FiniteAutomaton.FiniteAutomatonBase import FiniteAutomatonBase
from FiniteAutomaton.Edge import Edge


def remove_empty_edges(automaton: FiniteAutomatonBase) -> FiniteAutomatonBase:
    processed_vertices: Set = set()
    copy = FiniteAutomatonBase(list(), automaton.terminals, automaton.alphabet, automaton.start)

    def _dfs(vertex: str, root: str):
        processed_vertices.add(vertex)

        if vertex not in automaton.graph.keys():
            return

        for edge in automaton.graph[vertex]:
            if edge.end == vertex and edge.value != '':
                copy.add_edge(Edge(root, edge.end, edge.value))
            if edge.end in processed_vertices:
                continue
            if edge.value == '':
                if edge.end in automaton.terminals:
                    copy.terminals.add(root)
                _dfs(vertex=edge.end, root=root)
            else:
                copy.add_edge(Edge(root, edge.end, edge.value))

    for key in automaton.graph.keys():
        processed_vertices.clear()
        _dfs(key, key)
    return copy
