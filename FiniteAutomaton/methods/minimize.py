from typing import List, Dict, Tuple, Set
from copy import deepcopy

from FiniteAutomaton.Edge import Edge
from FiniteAutomaton.FiniteAutomatonBase import FiniteAutomatonBase


def _build_graph(
        copy: FiniteAutomatonBase,
        automaton: FiniteAutomatonBase,
        state: Dict[str, List[List[str]]],
        mask: Dict[str, str],
):
    copy.start = '0'

    used_edges: Set[Tuple[str, str, str]] = set()
    for key in state:
        for edge in state[key]:
            if key in automaton.terminals:
                copy.terminals.add(mask[key])
            if len(edge) >= 2:
                edge_tuple = (mask[key], edge[1], edge[0])
                if edge_tuple not in used_edges:
                    used_edges.add(edge_tuple)
                    copy.add_edge(Edge(mask[key], edge[1], edge[0]))


def _calculate_next_state(
        next_state: Dict[str, List[List[str]]],
        automaton: FiniteAutomatonBase,
        mask: Dict[str, str],
):
    for vertex in automaton.graph.keys():
        next_state[vertex] = [[mask[vertex]]]
        for edge in automaton.graph[vertex]:
            if vertex in next_state.keys():
                next_state[vertex].append([edge.value, mask[edge.end]])
            else:
                next_state[vertex] = [[edge.value, mask[edge.end]]]
        if vertex in next_state.keys():
            next_state[vertex].sort()


def minimize(deterministic_automaton: FiniteAutomatonBase) -> FiniteAutomatonBase:
    automaton: FiniteAutomatonBase = deepcopy(deterministic_automaton)
    automaton.reindex_vertices()
    automaton.add_empty_keys()

    mask: Dict[str, str] = {}
    copy = FiniteAutomatonBase([], set(), [], '0')

    for key in automaton.graph.keys():
        mask[key] = '0' if key in automaton.terminals else '1'

    while True:
        next_state: Dict[str, List[List[str]]] = {}
        _calculate_next_state(next_state, automaton, mask)

        reindex_map: Dict[str] = {}
        index: int = 0
        is_finished: bool = True
        for key in next_state:
            if str(next_state[key]) not in reindex_map.keys():
                reindex_map[str(next_state[key])] = str(index)
                index += 1
            if reindex_map[str(next_state[key])] != mask[key]:
                is_finished = False
        if is_finished:
            _build_graph(copy, automaton, next_state, mask)
            break

        mask = {}
        for key in next_state.keys():
            mask[key] = reindex_map[str(next_state[key])]

    return copy
