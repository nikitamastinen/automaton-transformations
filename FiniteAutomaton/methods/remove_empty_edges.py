from typing import Set

from FiniteAutomaton.FiniteAutomatonBase import FiniteAutomatonBase
from FiniteAutomaton.Edge import Edge


def remove_empty_edges(automaton: FiniteAutomatonBase) -> FiniteAutomatonBase:
    used: Set = set()
    copy = FiniteAutomatonBase(list(), automaton.terminals, automaton.alphabet, automaton.start)

    def _dfs(v: str, root: str):
        used.add(v)

        if v not in automaton.graph.keys():
            return

        for e in automaton.graph[v]:
            if e.end == v and e.value != '':
                copy.add_edge(Edge(root, e.end, e.value))
            if e.end in used:
                continue
            if e.value == '':
                if e.end in automaton.terminals:
                    copy.terminals.add(root)
                _dfs(e.end, root)
            else:
                copy.add_edge(Edge(root, e.end, e.value))

    for key in automaton.graph.keys():
        used.clear()
        _dfs(key, key)
    return copy
