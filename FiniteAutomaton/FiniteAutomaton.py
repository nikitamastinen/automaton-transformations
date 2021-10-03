from typing import Dict, Any

from FiniteAutomaton.FiniteAutomatonBase import FiniteAutomatonBase

from FiniteAutomaton.methods.get_regular_expression import get_regular_expression
from FiniteAutomaton.methods.minimize import minimize
from FiniteAutomaton.methods.remove_empty_edges import remove_empty_edges
from FiniteAutomaton.methods.determinate import determinate
from FiniteAutomaton.methods.complete_edges import complete_edges
from FiniteAutomaton.methods.reverse import reverse


class FiniteAutomaton:
    def __init__(self, *args, **kwargs) -> None:
        self.base = FiniteAutomatonBase(*args, **kwargs)

    def remove_empty_value_edges(self) -> None:
        self.base = remove_empty_edges(self.base)

    def convert_to_deterministic_automaton(self) -> None:
        self.base = determinate(self.base)

    def add_missing_edges(self) -> None:
        self.base = complete_edges(self.base)

    def complement(self) -> None:
        self.base = reverse(self.base)

    def minimize(self) -> None:
        self.base = minimize(self.base)

    def get_regular_expression(self) -> str:
        return get_regular_expression(self.base)

    def print(self) -> None:
        self.base.print()

    def dict(self) -> Dict[str, Any]:
        return self.base.dict()
