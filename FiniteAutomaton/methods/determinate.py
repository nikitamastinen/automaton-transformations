from typing import List, Set

from FiniteAutomaton.Edge import Edge
from FiniteAutomaton.FiniteAutomatonBase import FiniteAutomatonBase
from queue import Queue


def _hash_vertex(elements: List[str]) -> str:
    elements = [*frozenset(elements)]
    elements.sort()
    return str(elements)


def determinate(automaton: FiniteAutomatonBase) -> FiniteAutomatonBase:
    queue: Queue[List] = Queue()
    processed_vertices: Set[str] = set()
    copy = FiniteAutomatonBase(list(), set(), automaton.alphabet, automaton.start)

    copy.start = _hash_vertex([copy.start])
    queue.put([automaton.start])
    processed_vertices.add(_hash_vertex([automaton.start]))
    if automaton.start in automaton.terminals:
        copy.terminals.add(copy.start)

    while not queue.empty():
        vertices: List[str] = queue.get()
        processed_vertices.add(_hash_vertex(vertices))
        for symbol in automaton.alphabet:
            state: List[str] = []
            is_terminal = False
            for vertex in vertices:
                if vertex not in automaton.graph.keys():
                    continue
                for to in automaton.graph[vertex]:
                    if to.value == symbol:
                        is_terminal |= (to.end in automaton.terminals)
                        state.append(to.end)
            if len(state) < 1:
                continue
            if _hash_vertex(state) not in processed_vertices:
                queue.put(state)

            edge = Edge(_hash_vertex(vertices), _hash_vertex(state), symbol)
            copy.add_edge(edge)
            if is_terminal:
                copy.terminals.add(_hash_vertex(state))
    copy.reindex_vertices()
    return copy
