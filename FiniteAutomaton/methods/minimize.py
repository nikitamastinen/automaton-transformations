from typing import List, Dict, Tuple, Set
from copy import deepcopy

from FiniteAutomaton.Edge import Edge
from FiniteAutomaton.FiniteAutomatonBase import FiniteAutomatonBase
from FiniteAutomaton.methods.complete_edges import complete_edges


def minimize(deterministic_automaton: FiniteAutomatonBase) -> FiniteAutomatonBase:
    automaton: FiniteAutomatonBase = deepcopy(deterministic_automaton)
    automaton.reindex_vertices()
    automaton.add_empty_keys()

    mask: Dict[str, str] = {}

    copy = FiniteAutomatonBase([], set(), [], '0')

    for i in automaton.graph.keys():
        if i in automaton.terminals:
            mask[i] = '0'
        else:
            mask[i] = '1'
    while True:
        next_state: Dict[str, List[List[str]]] = {}
        for v in automaton.graph.keys():
            next_state[v] = [[mask[v]]]
            for e in automaton.graph[v]:
                if v in next_state.keys():
                    next_state[v].append([e.value, mask[e.end]])
                else:
                    next_state[v] = [[e.value, mask[e.end]]]
            if v in next_state.keys():
                next_state[v].sort()

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
            copy.start = '0'

            used: Set[Tuple[str, str, str]] = set()
            for key in next_state:
                for i in next_state[key]:
                    if key in automaton.terminals:
                        copy.terminals.add(mask[key])
                    if len(i) >= 2:
                        edge_tuple = (mask[key], i[1], i[0])
                        if edge_tuple not in used:
                            used.add(edge_tuple)
                            copy.add_edge(Edge(mask[key], i[1], i[0]))
            break

        mask = {}
        for key in next_state.keys():
            mask[key] = reindex_map[str(next_state[key])]

    return copy
