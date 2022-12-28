from typing import Optional, Iterable

from utils import read_data
import time


class Node:
    value: int
    prev: 'Node'
    next: 'Node'

    def __init__(self, value: int):
        self.value = value
        self.prev = self.next = self

    def __repr__(self):
        return f"Node({self.value})"


class File:
    def __init__(self, raw_input: str):
        ints = [int(x) for x in raw_input.splitlines()]
        self.start_node = Node(ints[0])
        self.original_order = [self.start_node]
        self.zero_node = None
        for item in ints[1:]:
            to_append = Node(item)
            to_append.next = self.start_node
            to_append.prev = self.start_node.prev
            self.start_node.prev.next = to_append
            self.start_node.prev = to_append
            self.original_order.append(to_append)
            if item == 0:
                self.zero_node = to_append

    def traverse_nodes(self) -> Iterable[Node]:
        yield self.start_node
        current = self.start_node.next
        while current is not self.start_node:
            yield current
            current = current.next

    def process_node(self, node: Node):
        if node.value == 0:
            return
        if node is self.start_node:
            self.start_node = node.next
        amount_to_move = node.value % (len(self.original_order)-1)
        node_to_insert_after = node
        for _ in range(amount_to_move):
            node_to_insert_after = node_to_insert_after.next
        # Excise the node from the chain
        node.prev.next = node.next
        node.next.prev = node.prev
        # Reconfigure the node to be after node_to_insert_after
        node.next = node_to_insert_after.next
        node.prev = node_to_insert_after
        # Tell the list the node is there
        node_to_insert_after.next.prev = node
        node_to_insert_after.next = node

    def decrypt_file(self):
        # self.print_nodes()
        for node in self.original_order:
            self.process_node(node)
            # self.print_nodes()

    def get_coordinates(self):
        assert self.zero_node is not None
        coord_moves = 1000 % (len(self.original_order))
        current = self.zero_node
        coord_total = 0
        for _ in range(3):
            for _ in range(coord_moves):
                current = current.next
            coord_total += current.value
        return coord_total

    def print_nodes(self):
        print(", ".join(str(x.value) for x in self.traverse_nodes()))


TEST = """1
2
-3
3
-2
0
4"""


def main():
    efile = File(read_data())
    efile.decrypt_file()
    print(f"Part one: {efile.get_coordinates()}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
