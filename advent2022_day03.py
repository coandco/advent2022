from utils import read_data


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args, strict=True)


INPUT = read_data().split("\n")
MAPPING = {chr(x): x - 96 for x in range(97, 123)}
MAPPING.update({chr(x): x - 38 for x in range(65, 91)})


def main():
    # Get the intersection of the first half of the string and the second half of the string
    common_elements = [(set(x[:len(x) // 2]) & set(x[len(x) // 2:])).pop() for x in INPUT]
    print(f"Part one: {sum(MAPPING[x] for x in common_elements)}")
    # Get the intersection of all three strings
    common_elements = [(set(x[0]) & set(x[1]) & set(x[2])).pop() for x in grouper(INPUT, 3)]
    print(f"Part two: {sum(MAPPING[x] for x in common_elements)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

