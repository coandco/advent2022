from typing import Tuple
from utils import read_data
import time


# Taken from https://stackoverflow.com/a/2657733
def insert_newlines(string, every=40):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))


# Taken from advent-of-code-ocr
ALPHABET_6 = {
    " ██ \n█  █\n█  █\n████\n█  █\n█  █": "A",
    "███ \n█  █\n███ \n█  █\n█  █\n███ ": "B",
    " ██ \n█  █\n█   \n█   \n█  █\n ██ ": "C",
    "████\n█   \n███ \n█   \n█   \n████": "E",
    "████\n█   \n███ \n█   \n█   \n█   ": "F",
    " ██ \n█  █\n█   \n█ ██\n█  █\n ███": "G",
    "█  █\n█  █\n████\n█  █\n█  █\n█  █": "H",
    " ███\n  █ \n  █ \n  █ \n  █ \n ███": "I",
    "  ██\n   █\n   █\n   █\n█  █\n ██ ": "J",
    "█  █\n█ █ \n██  \n█ █ \n█ █ \n█  █": "K",
    "█   \n█   \n█   \n█   \n█   \n████": "L",
    " ██ \n█  █\n█  █\n█  █\n█  █\n ██ ": "O",
    "███ \n█  █\n█  █\n███ \n█   \n█   ": "P",
    "███ \n█  █\n█  █\n███ \n█ █ \n█  █": "R",
    " ███\n█   \n█   \n ██ \n   █\n███ ": "S",
    "█  █\n█  █\n█  █\n█  █\n█  █\n ██ ": "U",
    "█   \n█   \n █ █\n  █ \n  █ \n  █ ": "Y",
    "████\n   █\n  █ \n █  \n█   \n████": "Z",
}


# Taken from advent-of-code-ocr
def ocr(input: str) -> str:
    lines = input.splitlines()
    indices = [slice(start, start + 4) for start in range(0, len(lines[0]), 5)]
    result = [
        ALPHABET_6["\n".join("".join(row[index]) for row in lines)]
        for index in indices
    ]
    return "".join(result)


def sprite_visible(cycle: int, x: int):
    return (cycle % 40) in (x-1, x, x+1)


def execute_instruction(x: int, instruction: str, part_two=False) -> Tuple[int, int]:
    if instruction.startswith("noop"):
        return x, 1
    elif instruction.startswith("addx"):
        arg = int(instruction.split(" ")[1])
        return x + arg, 2
    else:
        raise Exception(f"Unknown instruction {instruction}!")


def main():
    # Initialize the 0th item to the starting value, since cycle starts on 1
    x_values = [1]
    x = 1
    for line in read_data().splitlines():
        new_x, cycles_taken = execute_instruction(x, line)
        x_values += [x] * cycles_taken
        x = new_x
    print(f"Part one: {sum(x_values[v] * v for v in range(20, 221, 40))}")
    output_str = insert_newlines(''.join("█" if sprite_visible(i, x) else " " for i, x in enumerate(x_values[1:])))
    print(f"Part two: {ocr(output_str)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
