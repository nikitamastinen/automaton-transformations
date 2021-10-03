from FiniteAutomaton.FiniteAutomaton import FiniteAutomaton


def test_remove_empty_value_edges1():
    finite_automaton: FiniteAutomaton = FiniteAutomaton(
        [
            ('1', '2', ''),
            ('1', '4', 'b'),
            ('2', '3', 'a'),
            ('2', '5', ''),
        ],
        {'1', '2', '5'},
        ['a', 'b'],
        '1',
    )
    finite_automaton.remove_empty_value_edges()

    assert finite_automaton.dict() == {
        'head': '1',
        'edges': [
            ('1', '3', 'a'),
            ('1', '4', 'b'),
            ('2', '3', 'a')
        ],
        'terminals': ['1', '2', '5']
    }


def test_remove_empty_value_edges2():
    finite_automaton: FiniteAutomaton = FiniteAutomaton(
        [
            ('1', '1', ''),
        ],
        {'1'},
        ['a', 'b'],
        '1',
    )
    finite_automaton.remove_empty_value_edges()
    finite_automaton.print()
    assert finite_automaton.dict() == {
        'head': '1',
        'edges': [],
        'terminals': ['1'],
    }
