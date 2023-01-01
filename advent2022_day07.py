from typing import Dict, Tuple, List, Iterable
from pathlib import Path
from utils import read_data


def affected_folders(node: Path) -> Iterable[Path]:
    while True:
        yield node
        if node.parent == node:
            break
        node = node.parent


def parse_ls(ls_output: str) -> Tuple[List[str], int]:
    children = []
    my_size = 0
    for line in ls_output.splitlines()[1:]:
        tag, name = line.split(" ", maxsplit=1)
        if tag == "dir":
            children.append(name)
        else:
            my_size += int(tag)
    return children, my_size


def parse_input(full_input: str) -> Dict[Path, int]:
    sizes = {Path("/"): 0}
    current_node = Path("/")
    commands = full_input.split("$ ")
    # When you split on $ and the file starts with it, you have a blank line to start with
    for command in commands[1:]:
        if command.startswith("cd"):
            name = command.split(" ", maxsplit=1)[-1].strip()
            if name == "..":
                current_node = current_node.parent
            elif name == "/":
                current_node = Path("/")
            else:
                current_node = current_node / name
        elif command.startswith("ls"):
            children, size = parse_ls(command)
            sizes |= {current_node/x: 0 for x in children}
            for node in affected_folders(current_node):
                sizes[node] += size
        else:
            raise Exception(f"Unknown command {command}")
    return sizes


def main():
    size_dict = parse_input(read_data())
    print(f"Part one: {sum(x for x in size_dict.values() if x < 100000)}")
    free_space = 70000000 - size_dict[Path("/")]
    space_needed = 30000000
    threshold_to_free = space_needed - free_space
    print(f"Part two: {min(x for x in size_dict.values() if x > threshold_to_free)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")





