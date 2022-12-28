import math
from collections import deque

from utils import read_data
from typing import NamedTuple, Deque, Iterable
import re
import time

DIGITS = re.compile(r"\d+")


class State(NamedTuple):
    time_left: int
    ore_bots: int
    clay_bots: int
    obsidian_bots: int
    ore: int
    clay: int
    obsidian: int
    geodes: int

    def modify(self, **kwargs) -> "State":
        return State(**{x: getattr(self, x) + kwargs.get(x, 0) for x in self._fields})


class Blueprint:
    id: int
    orebot_ore: int
    claybot_ore: int
    obsidianbot_ore: int
    obsidianbot_clay: int
    geodebot_ore: int
    geodebot_obsidian: int

    def __init__(self, raw_line: str):
        raw_parsed = DIGITS.findall(raw_line)
        self.id = int(raw_parsed[0])
        self.orebot_ore = int(raw_parsed[1])
        self.claybot_ore = int(raw_parsed[2])
        self.obsidianbot_ore, self.obsidianbot_clay = (int(x) for x in raw_parsed[3:5])
        self.geodebot_ore, self.geodebot_obsidian = (int(x) for x in raw_parsed[5:7])
        self.max_orebots_needed = max(self.orebot_ore, self.claybot_ore, self.obsidianbot_ore, self.geodebot_ore)
        self.max_claybots_needed = self.obsidianbot_clay
        self.max_obsidianbots_needed = self.geodebot_obsidian


    def possible_actions(self, state: State) -> Iterable[State]:
        # First, try to build an ore bot if we're not already at max
        if state.ore_bots < self.max_orebots_needed:
            ore_needed = max(self.orebot_ore - state.ore, 0)
            time_taken = math.ceil(ore_needed / state.ore_bots) + 1
            if time_taken < state.time_left:
                yield state.modify(
                    time_left=-time_taken,
                    ore_bots=+1,
                    ore=(state.ore_bots * time_taken) - self.orebot_ore,
                    clay=state.clay_bots * time_taken,
                    obsidian=state.obsidian_bots * time_taken
                )

        # Second, try to build a clay bot if we're not already at max
        if state.clay_bots < self.max_claybots_needed:
            ore_needed = max(self.claybot_ore - state.ore, 0)
            time_taken = math.ceil(ore_needed / state.ore_bots) + 1
            if time_taken < state.time_left:
                yield state.modify(
                    time_left=-time_taken,
                    clay_bots=+1,
                    ore=(state.ore_bots * time_taken) - self.claybot_ore,
                    clay=state.clay_bots * time_taken,
                    obsidian=state.obsidian_bots * time_taken
                )

        # Third, try to build an obsidian bot if we're not already at max and are producing any clay
        if state.obsidian_bots < self.max_obsidianbots_needed and state.clay_bots > 0:
            ore_needed = max(self.obsidianbot_ore - state.ore, 0)
            clay_needed = max(self.obsidianbot_clay - state.clay, 0)
            time_for_ore = math.ceil(ore_needed / state.ore_bots) + 1
            time_for_clay = math.ceil(clay_needed / state.clay_bots) + 1
            time_taken = max(time_for_ore, time_for_clay)
            if time_taken < state.time_left:
                yield state.modify(
                    time_left=-time_taken,
                    obsidian_bots=+1,
                    ore=(state.ore_bots * time_taken) - self.obsidianbot_ore,
                    clay=(state.clay_bots * time_taken) - self.obsidianbot_clay,
                    obsidian=state.obsidian_bots * time_taken
                )

        # Finally, try to build a geode bot if we're producing any obsidian
        if state.obsidian_bots > 0:
            ore_needed = max(self.geodebot_ore - state.ore, 0)
            obsidian_needed = max(self.geodebot_obsidian - state.obsidian, 0)
            time_for_ore = math.ceil(ore_needed / state.ore_bots) + 1
            time_for_obsidian = math.ceil(obsidian_needed / state.obsidian_bots) + 1
            time_taken = max(time_for_ore, time_for_obsidian)
            if time_taken < state.time_left:
                yield state.modify(
                    time_left=-time_taken,
                    ore=(state.ore_bots * time_taken) - self.geodebot_ore,
                    clay=state.clay_bots * time_taken,
                    obsidian=(state.obsidian_bots * time_taken) - self.geodebot_obsidian,
                    geodes=state.time_left - time_taken
                )


def get_max_geodes(blueprint: Blueprint, minutes_remaining: int = 24) -> int:
    # Start with a single ore bot and n minutes remaining
    starting_state = State(minutes_remaining, 1, 0, 0, 0, 0, 0, 0)
    work_queue: Deque[State] = deque([starting_state])
    max_geodes = 0
    while len(work_queue) > 0:
        state = work_queue.pop()
        max_geodes = max(max_geodes, state.geodes)
        work_queue.extend(blueprint.possible_actions(state))

    return max_geodes



TEST = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian"""


def main():
    parsed = [Blueprint(x) for x in TEST.splitlines()]
    max_geodes = [get_max_geodes(x) for x in parsed]
    print(f"Part one: {sum(x*i for i, x in enumerate(max_geodes, start=1))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
