from collections import deque
from typing import Iterable, Tuple, Set, Dict, Deque, List
from typing_extensions import Self
from itertools import combinations
import re
from utils import read_data, BaseCoord

DIGITS = re.compile(r'-?\d+')


class Coord(BaseCoord):
    def all_in_row(self, distance: int, row: int) -> range:
        row_distance = abs(self.y - row)
        valid_x_range = distance - row_distance
        return range(self.x-valid_x_range, self.x+valid_x_range+1)

    def get_compass_point(self, other: Self) -> Self:
        diff = other - self
        return self.__class__(x=diff.x//abs(diff.x) if diff.x else 0, y=diff.y//abs(diff.y) if diff.y else 0)

    def all_at_manhattan(self, other: Self, distance: int) -> Iterable[Self]:
        compass_point = self.get_compass_point(other)
        if compass_point.x == 0 or compass_point.y == 0:
            yield self + Coord(x=distance * compass_point.x, y=distance * compass_point.y)
        else:
            for x in range(0, distance+1):
                y = distance - x
                yield self + Coord(x=x * compass_point.x, y=y * compass_point.y)

    def in_range(self, other: Self, distance: int) -> bool:
        return self.distance(other) <= distance


def parse_input(raw_input: str) -> Tuple[Dict[Coord, int], Set[Coord]]:
    known_beacons = set()
    sensors = {}
    for line in raw_input.splitlines():
        sensor_x, sensor_y, beacon_x, beacon_y = DIGITS.findall(line)
        sensor, beacon = Coord(x=int(sensor_x), y=int(sensor_y)), Coord(x=int(beacon_x), y=int(beacon_y))
        known_beacons.add(beacon)
        sensors[sensor] = sensor.distance(beacon)
    return sensors, known_beacons


def merge_ranges(ranges: List[range]) -> List[range]:
    ranges_q: Deque[range] = deque(sorted(ranges, key=lambda x: x.start))
    merged_ranges = []
    while ranges_q and (merge_to := ranges_q.popleft()):
        # We expand the range by one to allow for merging of adjacent ranges that don't overlap
        while ranges_q and ranges_q[0].start in merge_to:
            merge_from = ranges_q.popleft()
            merge_to = range(merge_to.start, max(merge_to.stop, merge_from.stop))
        merged_ranges.append(merge_to)
    return merged_ranges


def candidates(sensors: Dict[Coord, int]) -> Iterable[Coord]:
    for first, second in combinations(sensors, 2):
        if first.distance(second) == sensors[first] + sensors[second] + 2:
            larger, smaller = (first, second) if sensors[first] >= sensors[second] else (second, first)
            yield from smaller.all_at_manhattan(larger, sensors[smaller]+1)


def valid_location(location: Coord, sensors: Dict[Coord, int], known_beacons: Set[Coord], max_xy: int = 20) -> bool:
    if location.x < 0 or location.x > max_xy or location.y < 0 or location.y > max_xy:
        return False
    if location in known_beacons:
        return False
    return all(location.distance(sensor) > distance for sensor, distance in sensors.items())


def main():
    sensors, known_beacons = parse_input(read_data())
    row_to_check = 2000000
    ranges = merge_ranges([row_in_range for x in sensors if (row_in_range := x.all_in_row(sensors[x], row_to_check))])
    beacons_in_ranges = [x for x in known_beacons if x.y == row_to_check and any(x.x in rng for rng in ranges)]
    print(f"Part one: {sum(len(x) for x in ranges)-len(beacons_in_ranges)}")
    unknown_beacon_loc = next(x for x in candidates(sensors) if valid_location(x, sensors, known_beacons, 4000000))
    print(f"Part two: {unknown_beacon_loc.x*4000000 + unknown_beacon_loc.y}")


if __name__ == '__main__':
    main()


