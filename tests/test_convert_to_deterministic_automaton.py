from FiniteAutomaton.FiniteAutomaton import FiniteAutomaton


def test_convert_to_deterministic_automaton1():
    finite_automaton: FiniteAutomaton = FiniteAutomaton(
        [
            ('1', '2', 'a'),
            ('1', '3', 'a'),
            ('3', '4', 'b'),
            ('2', '2', 'b'),
            ('2', '4', 'a'),
        ],
        {'4'},
        ['a', 'b'],
        '1',
    )
    finite_automaton.convert_to_deterministic_automaton()

    assert finite_automaton.dict() == {
        'head': '0',
        'edges': [
            ('0', '1', 'a'),
            ('1', '2', 'b'),
            ('1', '4', 'a'),
            ('2', '3', 'b'),
            ('2', '4', 'a'),
            ('3', '3', 'b'),
            ('3', '4', 'a')
        ],
        'terminals': ['2', '4']
    }


def test_convert_to_deterministic_automaton2():
    finite_automaton: FiniteAutomaton = FiniteAutomaton(
        [
            ('1', '1', ''),
        ],
        {'1'},
        ['a', 'b'],
        '1',
    )
    finite_automaton.remove_empty_value_edges()
    finite_automaton.convert_to_deterministic_automaton()
    finite_automaton.print()
    assert finite_automaton.dict() == {
        'head': '0',
        'edges': [],
        'terminals': ['0'],
    }
