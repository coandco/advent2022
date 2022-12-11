from typing import List, Union
from math import prod
import re

from utils import read_data

PARSE_REGEX = re.compile(r'Monkey (?P<monkey_num>\d):\n'
                         r'  Starting items: (?P<items>.*$)\n'
                         r'  Operation: new = old (?P<op>.) (?P<operand>.*$)\n'
                         r'  Test: divisible by (?P<test_div>.*$)\n'
                         r'    If true: throw to monkey (?P<true_throw>.*$)\n'
                         r'    If false: throw to monkey (?P<false_throw>.*$)', re.MULTILINE)


class Monkey:
    def __init__(self, raw_monkey: str):
        match = PARSE_REGEX.match(raw_monkey).groupdict()
        self.monkeynum = int(match["monkey_num"])
        self.items = [int(x) for x in match["items"].split(", ")]
        self.op = match["op"]
        self.operand = "old" if match["operand"] == "old" else int(match["operand"])
        self.test_div = int(match["test_div"])
        self.true_throw = int(match["true_throw"])
        self.false_throw = int(match["false_throw"])
        self.lcm = None
        self.inspection_counter = 0

    def apply_op(self, worry_level: Union[int, str]) -> int:
        operand = worry_level if self.operand == "old" else self.operand
        if self.op == '*':
            return worry_level * operand
        elif self.op == "+":
            return worry_level + operand
        else:
            raise Exception(f"Unknown operator f{self.op}")

    def handle_items(self, monkeys: List['Monkey']):
        for item in self.items:
            self.inspection_counter += 1
            worry_level = self.apply_op(item)
            if self.lcm:
                worry_level = worry_level % self.lcm
            else:
                worry_level = worry_level // 3
            throw_to = self.true_throw if worry_level % self.test_div == 0 else self.false_throw
            monkeys[throw_to].items.append(worry_level)
        self.items = []


if __name__ == '__main__':
    monkeys = [Monkey(x) for x in read_data().split("\n\n")]
    for _ in range(20):
        for monkey in monkeys:
            monkey.handle_items(monkeys)
    most_active_monkeys = sorted([x.inspection_counter for x in monkeys], reverse=True)
    print(f"Part one: {most_active_monkeys[0] * most_active_monkeys[1]}")
    monkeys = [Monkey(x) for x in read_data().split("\n\n")]
    lcm = prod(x.test_div for x in monkeys)
    for monkey in monkeys:
        monkey.lcm = lcm
    for i in range(10000):
        for monkey in monkeys:
            monkey.handle_items(monkeys)
    most_active_monkeys = sorted([x.inspection_counter for x in monkeys], reverse=True)
    print(f"Part two: {most_active_monkeys[0] * most_active_monkeys[1]}")

