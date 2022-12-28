from collections import deque

from utils import read_data
from typing import NamedTuple, Deque, Iterable, Dict
import re
import time

DIGITS = re.compile(r"\d+")


class State(NamedTuple):
    minutes: int
    ore_bots: int
    clay_bots: int
    obsidian_bots: int
    ore: int
    clay: int
    obsidian: int
    geodes: int

    def possible_actions(self, blueprint: "Blueprint") -> Iterable["State"]:
        max_orebots_needed = max(blueprint.ore_ore, blueprint.clay_ore, blueprint.obsidian_ore, blueprint.geode_ore)
        max_claybots_needed = blueprint.obsidian_clay
        max_obsidianbots_needed = blueprint.geode_obsidian
        # First, we could do nothing and just collect materials
        yield self.modify(
            time=+1, ore=self.ore_bots, clay=self.clay_bots, obsidian=self.obsidian_bots
        )
        # We could build an ore bot
        if self.ore >= blueprint.ore_ore and self.ore_bots < max_orebots_needed:
            yield self.modify(
                time=+1,
                ore_bots=+1,
                ore=self.ore_bots - blueprint.ore_ore,
                clay=self.clay_bots,
                obsidian=self.obsidian_bots
            )

        # We could build a clay bot
        if self.ore >= blueprint.clay_ore and self.clay_bots < max_claybots_needed:
            yield self.modify(
                time=+1,
                clay_bots=+1,
                ore=self.ore_bots - blueprint.clay_ore,
                clay=self.clay_bots,
                obsidian=self.obsidian_bots
            )

        # We could build an obsidian bot
        if self.ore >= blueprint.obsidian_ore and self.clay >= blueprint.obsidian_clay and self.obsidian_bots < max_obsidianbots_needed:
            yield self.modify(
                time=+1,
                obsidian_bots=+1,
                ore=self.ore_bots - blueprint.obsidian_ore,
                clay=self.clay_bots - blueprint.obsidian_clay,
                obsidian=self.obsidian_bots
            )

        # We could build a geode bot
        if self.ore >= blueprint.geode_ore and self.obsidian >= blueprint.geode_obsidian:
            yield self.modify(
                time=+1,
                geode_bots=+1,
                ore=self.ore_bots - blueprint.geode_ore,
                clay=self.clay_bots,
                obsidian=self.obsidian_bots - blueprint.geode_obsidian,
                geodes=self.minutes,
            )

    def modify(self, **kwargs) -> "State":
        return State(**{x: getattr(self, x) + kwargs.get(x, 0) for x in self._fields})


class Blueprint(NamedTuple):
    id: int
    ore_ore: int
    clay_ore: int
    obsidian_ore: int
    obsidian_clay: int
    geode_ore: int
    geode_obsidian: int

    @staticmethod
    def from_str(input_line: str) -> "Blueprint":
        return Blueprint(*(int(x) for x in DIGITS.findall(input_line)))


def get_max_geodes(blueprint: Blueprint, minutes_remaining: int = 24) -> int:
    starting_state = State(24, 1, 0, 0, 0, 0, 0, 0)
    work_queue: Deque[State] = deque([starting_state])
    max_geodes = 0
    best_state_at_time: Dict[int, State] = {}
    while len(work_queue) > 0:
        state = work_queue.pop()
        if state.minutes not in best_state_at_time or state.geodes > best_state_at_time[state.minutes].geodes:
            best_state_at_time[state.minutes] = state
        max_geodes = max(max_geodes, state.geodes)
        elif state.geodes >= best_state_at_time[state.minutes].geodes:
            work_queue.extend(state.possible_actions(blueprint))
    return max_geodes



TEST = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian"""


def main():
    parsed = [Blueprint.from_str(x) for x in TEST.splitlines()]
    max_geodes = [get_max_geodes(x) for x in parsed]
    print(max_geodes)


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
