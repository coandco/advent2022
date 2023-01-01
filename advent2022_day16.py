from typing import Dict, List, Tuple, NamedTuple, FrozenSet, Deque
from collections import defaultdict, deque
from itertools import combinations
from utils import read_data
import re

VALVE_REGEX = re.compile(
    r"^Valve (?P<name>[A-Z]*) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<tunnels>.*)$"
)
PathMapping = Dict[str, Dict[str, int]]


def find_shortest_paths(node: str, connections: Dict[str, List[str]]) -> Dict[str, int]:
    shortest_paths = defaultdict(lambda: 99999)
    work_queue = [(node, 0)]
    while len(work_queue) > 0:
        current, cost = work_queue.pop()
        if shortest_paths[current] <= cost:
            continue
        if cost > 0:
            shortest_paths[current] = cost
        work_queue.extend([(x, cost + 1) for x in connections[current]])
    return dict(shortest_paths)


def build_graph(raw_input: str) -> Tuple[Dict[str, int], PathMapping]:
    flow_rates: Dict[str, int] = {}
    connections: Dict[str, List[str]] = {}
    shortest_paths: PathMapping = {}

    # Build nodes
    for line in raw_input.splitlines():
        parsed = VALVE_REGEX.match(line).groupdict()
        if int(parsed["flow_rate"]) > 0:
            flow_rates[parsed["name"]] = int(parsed["flow_rate"])
        connections[parsed["name"]] = parsed["tunnels"].split(", ")

    # Precalculate shortest paths for non-null nodes
    for node in connections:
        shortest_paths[node] = {k: v for k, v in find_shortest_paths(node, connections).items() if k in flow_rates}

    return flow_rates, shortest_paths


class State(NamedTuple):
    time_left: int
    score: int
    current_loc: str
    valves_opened: FrozenSet[str]


def max_flow(
    flow_rates: Dict[str, int], shortest_paths: PathMapping, time_left: int = 30
) -> Dict[FrozenSet[str], int]:
    initial_state = State(time_left, score=0, current_loc="AA", valves_opened=frozenset())
    best_states: Dict[FrozenSet[str], int] = {}
    work_queue: Deque[State] = deque([initial_state])
    while len(work_queue) > 0:
        state = work_queue.pop()
        if state.score > best_states.get(state.valves_opened, 0):
            best_states[state.valves_opened] = state.score
        for new_loc in flow_rates:
            if new_loc in state.valves_opened:
                continue
            new_time = state.time_left - (shortest_paths[state.current_loc][new_loc] + 1)
            if new_time <= 0:
                continue
            # This is a valid path, add it to the queue
            new_state = State(
                time_left=new_time,
                score=state.score + (new_time * flow_rates[new_loc]),
                current_loc=new_loc,
                valves_opened=state.valves_opened | {new_loc},
            )
            work_queue.append(new_state)
    return best_states


def main():
    flow_rates, shortest_paths = build_graph(read_data())
    solutions = max_flow(flow_rates, shortest_paths, time_left=30)
    print(f"Part one: {max(solutions.values())}")
    solutions = max_flow(flow_rates, shortest_paths, time_left=26)
    # Find all non-overlapping pairs in the solutions and add their total point values
    joint_solutions = [solutions[x[0]] + solutions[x[1]] for x in combinations(solutions, 2) if len(x[0] & x[1]) == 0]
    print(f"Part two: {max(joint_solutions)}")


if __name__ == "__main__":
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
