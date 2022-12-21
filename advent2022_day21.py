from contextlib import suppress
from typing import Tuple, Dict
from sympy import solve
from sympy.parsing.sympy_parser import parse_expr
from utils import read_data
import time


def parse_input(input_str: str, omit_humn: bool = False) -> Tuple[Dict[str, int], Dict[str, str]]:
    known_items: Dict[str, int] = {}
    unknown_items: Dict[str, str] = {}
    for line in input_str.splitlines():
        label, value = line.split(": ")
        if omit_humn and label == "humn":
            continue
        try:
            known_items[label] = int(value)
        except ValueError:
            unknown_items[label] = value
    return known_items, unknown_items


def resolve_items(known_items: Dict[str, int], unknown_items: Dict[str, str]) -> Tuple[Dict[str, int], Dict[str, str]]:
    while unknown_items:
        old_len = len(unknown_items)
        for label, value in unknown_items.items():
            with suppress(NameError):
                known_items[label] = int(eval(value, known_items))
        [unknown_items.pop(x, None) for x in known_items]
        if len(unknown_items) == old_len:
            break
    return known_items, unknown_items


def get_root_equation(known_items: Dict[str, int], unknown_items: Dict[str, str]) -> str:
    rolled_up_items: Dict[str, str] = {}
    while unknown_items:
        old_len = len(unknown_items)
        for label, value in unknown_items.items():
            sym1, op, sym2 = value.split(" ")
            if label == "root":
                op = "-"
            sym1 = "humn" if sym1 == "humn" else known_items.get(sym1, rolled_up_items.get(sym1, None))
            sym2 = "humn" if sym2 == "humn" else known_items.get(sym2, rolled_up_items.get(sym2, None))
            if sym1 is not None and sym2 is not None:
                rolled_up_items[label] = f"({sym1} {op} {sym2})"
        [unknown_items.pop(x, None) for x in rolled_up_items]
        if len(unknown_items) == old_len:
            break
    return rolled_up_items["root"]


def main():
    monkeys, _ = resolve_items(*parse_input(read_data()))
    print(f"Part one: {int(monkeys['root'])}")
    equation = get_root_equation(*resolve_items(*parse_input(read_data(), omit_humn=True)))
    print(f"Part two: {solve(parse_expr(equation))[0]}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
