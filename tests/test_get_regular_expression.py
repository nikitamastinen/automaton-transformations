from FiniteAutomaton.FiniteAutomaton import FiniteAutomaton


def test_get_regular_expression1():
    finite_automaton: FiniteAutomaton = FiniteAutomaton([
        (0, 1, 'a'),
        (1, 2, 'b'),
        (2, 2, 'a'),
        (2, 3, 'c'),
    ],
        {'1', '3'},
        ['a', 'b', 'c'],
        '0',
    )
    assert finite_automaton.get_regular_expression() == '(a1)+(((ab)(a)*c)1)'  # a+aba*c


def test_get_regular_expression2():
    finite_automaton: FiniteAutomaton = FiniteAutomaton([
        (0, 0, 'a'),
        (0, 1, 'b'),
        (1, 1, 'b'),
    ],
        {'1', '2'},
        ['a', 'b'],
        '0',
    )
    print(finite_automaton.get_regular_expression())
    assert finite_automaton.get_regular_expression() == '(a)*+(b(b)*1)'  # a*bb*
