from utils import read_data
from typing import NamedTuple

INPUT = [x.split(" ") for x in read_data().splitlines()]
ROCK = 0
PAPER = 1
SCISSORS = 2
ROTATIONS_TO_VICTORY_POINTS = {
    0: 3,
    1: 0,
    2: 6
}

CHAR_TO_SIGN = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}

CHAR_TO_ROTATIONS = {
    "X": 2,
    "Y": 0,
    "Z": 1
}


class Sign(NamedTuple):
    type: int

    def shape_score(self) -> int:
        return self.type + 1

    def get_relative_rotations(self, other: 'Sign') -> int:
        # Rotate myself so I'm at 0, rotate the other sign to match, then see how far ahead they are
        offset = 3 - self.type
        return (other.type + offset) % 3

    def outcome_score(self, other: 'Sign') -> int:
        return ROTATIONS_TO_VICTORY_POINTS[self.get_relative_rotations(other)]

    def total_score(self, other: 'Sign') -> int:
        return self.shape_score() + self.outcome_score(other)


class Round:
    def __init__(self, first: str, second: str):
        self.their_sign = Sign(CHAR_TO_SIGN[first])
        self.my_sign = Sign(CHAR_TO_SIGN[second])
        # Pick the sign that will win/draw/lose based on X/Y/Z
        self.part_two_sign = Sign((self.their_sign.type + CHAR_TO_ROTATIONS[second]) % 3)
        self.part_one_score = self.my_sign.total_score(self.their_sign)
        self.part_two_score = self.part_two_sign.total_score(self.their_sign)


def main():
    rounds = [Round(*x) for x in INPUT]
    print(f"Part one: {sum(x.part_one_score for x in rounds)}")
    print(f"Part two: {sum(x.part_two_score for x in rounds)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

