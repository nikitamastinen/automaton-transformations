from FiniteAutomaton.FiniteAutomaton import FiniteAutomaton


def test_minimize1():
    finite_automaton: FiniteAutomaton = FiniteAutomaton([
            (0, 1, 'a'),
            (1, 2, 'a'),
            (2, 0, 'a'),
            (3, 4, 'a'),
            (4, 5, 'a'),
            (5, 3, 'a'),
            (6, 7, 'a'),
            (7, 8, 'a'),
            (8, 6, 'a'),
            (0, 3, 'b'),
            (3, 6, 'b'),
            (6, 0, 'b'),
            (1, 4, 'b'),
            (4, 7, 'b'),
            (7, 1, 'b'),
            (2, 5, 'b'),
            (5, 8, 'b'),
            (8, 2, 'b'),
        ],
        {'0', '4', '8'},
        ['a', 'b'],
        '0',
    )
    finite_automaton.convert_to_deterministic_automaton()
    finite_automaton.remove_empty_value_edges()
    finite_automaton.add_missing_edges()
    finite_automaton.minimize()
    assert {
        'head': '0',
        'edges': [
            ('0', '1', 'a'),
            ('0', '2', 'b'),
            ('1', '0', 'b'),
            ('1', '2', 'a'),
            ('2', '0', 'a'),
            ('2', '1', 'b')
        ],
        'terminals': ['0']
    }


def test_minimize2():
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
    # finite_automaton.print()
    finite_automaton.add_missing_edges()
    finite_automaton.minimize()

    finite_automaton.print()
    assert finite_automaton.dict() == {
        'head': '0',
        'edges': [
            ('0', '1', 'a'),
            ('0', '1', 'b'),
            ('1', '1', 'a'),
            ('1', '1', 'b'),
        ],
        'terminals': ['0'],
    }
