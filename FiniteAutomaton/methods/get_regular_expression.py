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

    for i in automaton.terminals:
        automaton.add_edge(Edge(i, 'end', '1'))
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
            for e in loops:
                cyc += e.value + '+'
            cyc = cyc[:-1] + ')*'
        for x in inp:
            for y in out:
                automaton.add_edge(Edge(x.start, y.end, '(' + x.value + cyc + y.value + ')'))
        for e in inp:
            automaton.graph[e.start].remove(e)
        for e in out:
            automaton.graph[e.start].remove(e)
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
