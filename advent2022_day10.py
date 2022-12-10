from typing import Tuple, Optional, Union
from utils import read_data



PART_1_TRIGGERS = [20, 60, 100, 140, 180, 220]


def sprite_visible(cycle: int, x: int):
    return ((cycle-1) % 40) in (x-1, x, x+1)


def execute_instruction(cycle: int, x: int, instruction: str, part_two=False) -> Tuple[int, int, Optional[int], str]:
    triggered_signal_strength = None
    output = "#" if sprite_visible(cycle, x) else "."
    if cycle in PART_1_TRIGGERS:
        triggered_signal_strength = cycle * x

    if instruction.startswith("noop"):
        return cycle + 1, x, triggered_signal_strength, output
    elif instruction.startswith("addx"):
        arg = int(instruction.split(" ")[1])
        cycle += 1
        output += "#" if sprite_visible(cycle, x) else "."
        if cycle in PART_1_TRIGGERS and not part_two:
            triggered_signal_strength = cycle * x
        return cycle + 1, x + arg, triggered_signal_strength, output
    else:
        raise Exception(f"Unknown instruction {instruction}!")


# Taken from https://stackoverflow.com/a/2657733
def insert_newlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))


# Taken from advent-of-code-ocr
ALPHABET_6 = {
    ".##.\n#..#\n#..#\n####\n#..#\n#..#": "A",
    "###.\n#..#\n###.\n#..#\n#..#\n###.": "B",
    ".##.\n#..#\n#...\n#...\n#..#\n.##.": "C",
    "####\n#...\n###.\n#...\n#...\n####": "E",
    "####\n#...\n###.\n#...\n#...\n#...": "F",
    ".##.\n#..#\n#...\n#.##\n#..#\n.###": "G",
    "#..#\n#..#\n####\n#..#\n#..#\n#..#": "H",
    ".###\n..#.\n..#.\n..#.\n..#.\n.###": "I",
    "..##\n...#\n...#\n...#\n#..#\n.##.": "J",
    "#..#\n#.#.\n##..\n#.#.\n#.#.\n#..#": "K",
    "#...\n#...\n#...\n#...\n#...\n####": "L",
    ".##.\n#..#\n#..#\n#..#\n#..#\n.##.": "O",
    "###.\n#..#\n#..#\n###.\n#...\n#...": "P",
    "###.\n#..#\n#..#\n###.\n#.#.\n#..#": "R",
    ".###\n#...\n#...\n.##.\n...#\n###.": "S",
    "#..#\n#..#\n#..#\n#..#\n#..#\n.##.": "U",
    "#...\n#...\n.#.#\n..#.\n..#.\n..#.": "Y",
    "####\n...#\n..#.\n.#..\n#...\n####": "Z",
}


def ocr(input: str) -> str:
    lines = input.splitlines()
    indices = [slice(start, start + 4) for start in range(0, len(lines[0]), 5)]
    result = [
        ALPHABET_6["\n".join("".join(row[index]) for row in lines)]
        for index in indices
    ]
    return "".join(result)


if __name__ == '__main__':
    cycle = x = 1
    sampled_values = []
    output_str = ''
    for line in read_data().splitlines():
        cycle, x, sampled_value, chars_output = execute_instruction(cycle, x, line)
        if sampled_value is not None:
            sampled_values.append(sampled_value)
        output_str += chars_output
    print(f"Part one: {sum(sampled_values)}")
    print(f"Part two: {ocr(insert_newlines(output_str, 40))}")
