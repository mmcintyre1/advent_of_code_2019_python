from typing import List

from puzzle_input import parsed_puzzle_input


class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = None
        self.parent_name = parent

    def __str__(self):
        return f"Node: {self.name}, Parent: {self.parent}"


class NodeMap:
    def __init__(self, root):
        self.nodes = {root: Node(root, None)}
        self.root = self.nodes[root]
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

    def navigate_up(self, node, dest, path=None):
        if path is None:
            path = []

        if node.parent == dest:
            return

        path.append(node.parent)
        self.navigate_up(node.parent, dest, path)

        return path

    def find_common_parent(self, node_one, node_two):
        node_one_to_root = self.navigate_up(self.nodes[node_one], self.root)
        node_two_to_root = self.navigate_up(self.nodes[node_two], self.root)

        for first_node in node_one_to_root:
            for second_node in node_two_to_root:
                if first_node == second_node:
                    return second_node

    def navigate_between(self, node_one, node_two):
        common_parent = self.find_common_parent(node_one, node_two)
        node_one_jumps = len(self.navigate_up(self.nodes[node_one], common_parent))
        node_two_jumps = len(self.navigate_up(self.nodes[node_two], common_parent))

        return node_one_jumps + node_two_jumps


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
    orbit_counts = orbits.orbit_count
    jumps = orbits.navigate_between("YOU", "SAN")

    print(f"Part 1: {orbit_counts} orbits")
    print(f"Part 2: {jumps} jumps")


if __name__ == '__main__':
    main()
