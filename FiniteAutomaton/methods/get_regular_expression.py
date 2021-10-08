from copy import deepcopy
from typing import List

from FiniteAutomaton.Edge import Edge
from FiniteAutomaton.FiniteAutomatonBase import FiniteAutomatonBase
from FiniteAutomaton.methods.complete_edges import complete_edges
from FiniteAutomaton.methods.determinate import determinate
from FiniteAutomaton.methods.remove_empty_edges import remove_empty_edges


def get_regular_expression(deterministic_automaton: FiniteAutomatonBase) -> str:
    automaton = deepcopy(deterministic_automaton)
    automaton = remove_empty_edges(automaton)
    automaton = determinate(automaton)
    automaton = complete_edges(automaton)

    for vertex in automaton.terminals:
        automaton.add_edge(Edge(vertex, 'end', '1'))
    automaton.terminals = {'end'}
    automaton.reindex_vertices()

    for key in automaton.graph.keys():
        if key == automaton.start or key in automaton.terminals:
            continue
        inp: List[Edge] = []
        out: List[Edge] = []
        loops: List[Edge] = []

        for vertex in automaton.graph.keys():
            for edge in automaton.graph[vertex]:
                if edge.start == edge.end and edge.start == key:
                    loops.append(deepcopy(edge))
                    continue
                if edge.start != edge.end:
                    if edge.start == key:
                        out.append(deepcopy(edge))
                    if edge.end == key:
                        inp.append(deepcopy(edge))
        cyc = ''
        if len(loops) > 0:
            cyc = '('
            for edge in loops:
                cyc += edge.value + '+'
            cyc = cyc[:-1] + ')*'
        for start in inp:
            for end in out:
                automaton.add_edge(Edge(start.start, end.end, '(' + start.value + cyc + end.value + ')'))
        for edge in inp:
            automaton.graph[edge.start].remove(edge)
        for edge in out:
            automaton.graph[edge.start].remove(edge)
    result = '('
    for vertex in automaton.graph.keys():
        for edge in automaton.graph[vertex]:
            if edge.start == edge.end and edge.start == automaton.start:
                result += edge.value + '+'
    if result != '(':
        result = result[:-1] + ')*+'
    else:
        result = ''
    for vertex in automaton.graph.keys():
        for edge in automaton.graph[vertex]:
            if edge.start == automaton.start and edge.end in automaton.terminals:
                result += edge.value + '+'
    result = result[:-1]
    return result
