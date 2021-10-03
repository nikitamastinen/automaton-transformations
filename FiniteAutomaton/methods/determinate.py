from typing import List, Set

from FiniteAutomaton.Edge import Edge
from FiniteAutomaton.FiniteAutomatonBase import FiniteAutomatonBase
from queue import Queue


def _hash_vertex(elements: List[str]) -> str:
    elements = [*set(elements)]
    elements.sort()
    return str(elements)


def determinate(automaton: FiniteAutomatonBase) -> FiniteAutomatonBase:
    queue: Queue[List] = Queue()
    used: Set[str] = set()
    copy = FiniteAutomatonBase(list(), set(), automaton.alphabet, automaton.start)

    copy.start = _hash_vertex([copy.start])
    queue.put([automaton.start])
    used.add(_hash_vertex([automaton.start]))
    if automaton.start in automaton.terminals:
        copy.terminals.add(copy.start)

    while not queue.empty():
        vertex: List[str] = queue.get()
        used.add(_hash_vertex(vertex))
        for w in automaton.alphabet:
            state: List[str] = []
            is_terminal = False
            for v in vertex:
                if v not in automaton.graph.keys():
                    continue
                for to in automaton.graph[v]:
                    if to.value == w:
                        is_terminal |= (to.end in automaton.terminals)
                        state.append(to.end)
            if len(state) >= 1:
                if _hash_vertex(state) not in used:
                    queue.put(state)
                edge = Edge(_hash_vertex(vertex), _hash_vertex(state), w)
                copy.add_edge(edge)
                if is_terminal:
                    copy.terminals.add(_hash_vertex(state))
    copy.reindex_vertices()
    return copy
