from typing import Optional, Dict
from utils import read_data


class Node:
    def __init__(self, fullname: str, parent: Optional['Node']):
        self.fullname = fullname
        self.name = self.fullname.rsplit('/', maxsplit=1)[-1]
        self.parent = parent
        self.cached_size = 0
        self.files: Dict[str, int] = {}
        self.children: Dict[str, 'Node'] = {}

    def update_cached_size(self, amount_to_add: int):
        self.cached_size += amount_to_add
        if self.parent:
            self.parent.update_cached_size(amount_to_add)

    def parse_ls(self, ls_output: str):
        for line in ls_output.splitlines()[1:]:
            tag, name = line.split(" ", maxsplit=1)
            if tag == "dir":
                self.children[name] = Node(f"{self.fullname}/{name}", parent=self)
            else:
                self.files[name] = int(tag)
                self.update_cached_size(self.files[name])

    def build_size_dict(self, size_dict: Dict[str, int]):
        for child in self.children.values():
            size_dict[child.fullname] = child.cached_size
            child.build_size_dict(size_dict)

    def __repr__(self):
        return f"Node({self.fullname}, {self.cached_size})"


def parse_input(full_input: str) -> Node:
    root_node = current_node = Node('', parent=None)
    commands = full_input.split("$ ")
    # When you split on $ and the file starts with it, you have a blank line to start with
    for command in commands[1:]:
        if command.startswith("cd"):
            name = command.split(" ", maxsplit=1)[-1].strip()
            if name == "..":
                current_node = current_node.parent
            elif name == "/":
                current_node = root_node
            else:
                current_node = current_node.children[name]
        elif command.startswith("ls"):
            current_node.parse_ls(command)
        else:
            raise Exception(f"Unknown command {command}")
    return root_node


if __name__ == '__main__':
    root_node = parse_input(read_data())
    size_dict = {"/": root_node.cached_size}
    root_node.build_size_dict(size_dict)
    print(f"Part one: {sum(x for x in size_dict.values() if x < 100000)}")
    free_space = 70000000 - root_node.cached_size
    space_needed = 30000000
    threshold_to_free = space_needed - free_space
    print(f"Part two: {min(x for x in size_dict.values() if x > threshold_to_free)}")




