from typing import List

from puzzle_input import parsed_puzzle_input


class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = None
        self.parent_name = parent
        self.children = {}

    def __str__(self):
        return f"Node: {self.name}, Parent: {self.parent}, Children: {self.children}"


class NodeMap:
    def __init__(self, root):
        self.nodes = {root: Node(root, None)}
        self.hydrated = False
        self.orbit_count = 0

    def build_tree(self):
        for node_name, node in self.nodes.items():
            self._recurse_hydrate(node)
        self.hydrated = True

    def _recurse_hydrate(self, node):
        if node.parent_name:
            node.parent = self.nodes[node.parent_name]
            self.orbit_count += 1
            self._recurse_hydrate(node.parent)


def build_node_map(raw_orbits: List) -> NodeMap:
    orbits = NodeMap(root="COM")
    for orbit in raw_orbits:
        parent, name = orbit.split(")")
        node = Node(name, parent)
        orbits.nodes[node.name] = node

    return orbits


def main():
    orbits = build_node_map(parsed_puzzle_input)
    orbits.build_tree()
    print(orbits.orbit_count)


if __name__ == '__main__':
    main()
