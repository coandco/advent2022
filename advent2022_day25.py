from utils import read_data


SNAFU_DIGITS = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2
}

REVERSED_DIGITS = {v: k for k, v in SNAFU_DIGITS.items()}


def snafu_to_int(snafu: str) -> int:
    if snafu:
        num_left, my_part = snafu[:-1], snafu[-1]
        return snafu_to_int(num_left)*5 + SNAFU_DIGITS[my_part]
    return 0


def int_to_snafu(value: int) -> str:
    if value:
        num_left, my_part = divmod(value+2, 5)
        return int_to_snafu(num_left) + REVERSED_DIGITS[my_part-2]
    return ''


def main():
    summed_snafus = sum(snafu_to_int(x) for x in read_data().splitlines())
    print(f"Part one: {int_to_snafu(summed_snafus)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
