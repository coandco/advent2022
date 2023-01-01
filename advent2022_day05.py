from typing import List, NamedTuple
from copy import deepcopy
import string
from utils import read_data

import re

DIGITS = re.compile(r'\d+')
INPUT_PART1, INPUT_PART2 = read_data().split("\n\n")


def parse_part1(asciiart: str) -> List[List[str]]:
    lines = asciiart.splitlines()
    columns_that_matter = range(1, len(lines[0]), 4)
    # Prefill a blank 0 column that we'll ignore
    output = [[]]
    for column in columns_that_matter:
        stack = []
        for line in reversed(lines):
            if line[column] in string.ascii_uppercase:
                stack.append(line[column])
        output.append(stack)
    return output


class MoveInstruction(NamedTuple):
    amount: int
    fromstack: int
    tostack: int


def parse_part2(procedure: str) -> List[MoveInstruction]:
    return [MoveInstruction(*(int(y) for y in DIGITS.findall(x))) for x in procedure.splitlines()]


def move_boxes(stacks: List[List[str]], fromstack: int, tostack: int, amount: int = 1):
    if len(stacks[fromstack]) < amount:
        raise Exception(f"Tried to move from stack {fromstack}, which has insufficient boxes : {stacks}")
    # Save the boxes we're moving
    boxes_to_move = stacks[fromstack][-amount:]
    # Remove them from the stack
    stacks[fromstack] = stacks[fromstack][:-amount]
    # Add them to the new stack
    stacks[tostack].extend(boxes_to_move)


def main():
    part1_stacks = parse_part1(INPUT_PART1)
    part2_stacks = deepcopy(part1_stacks)
    instructions = parse_part2(INPUT_PART2)
    for instruction in instructions:
        for _ in range(instruction.amount):
            move_boxes(part1_stacks, instruction.fromstack, instruction.tostack, 1)
    print(f"Part one: {''.join(x[-1] for x in part1_stacks[1:] if len(x) > 0)}")
    for instruction in instructions:
        move_boxes(part2_stacks, instruction.fromstack, instruction.tostack, instruction.amount)
    print(f"Part two: {''.join(x[-1] for x in part2_stacks[1:] if len(x) > 0)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
