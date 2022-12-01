from utils import read_data

INPUT = [x.split("\n") for x in read_data().split("\n\n")]


if __name__ == '__main__':
    totals = [sum(int(food) for food in elf) for elf in INPUT]
    sorted_totals = sorted(totals, reverse=True)
    print(f"Part one: {sorted_totals[0]}")
    print(f"Part two: {sum(sorted_totals[:3])}")