import argparse
import collections
import time

from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Set

argparser = argparse.ArgumentParser()
argparser.add_argument('file')

start_time = time.time()


direction_adjustments = {
    'n': (-1, 0),
    'w': (0, -1),
    's': (1, 0),
    'e': (0, 1)
}


@dataclass(frozen=True)
class InputNode:
    row: int
    col: int
    weight: int

    def __lt__(self, other):
        if self.row != other.row:
            return self.row < other.row
        return self.col < other.col


class InputGrid:

    def __init__(self):
        self._map = {}
        self._max_row = self._max_col = -1

    def __len__(self):
        return self.height * self.width

    def add(self, node: InputNode):
        self._max_row = max(node.row, self._max_row)
        self._max_col = max(node.col, self._max_col)
        self._map[(node.row, node.col)] = node

    def get(self, row, col) -> InputNode:
        return self._map.get((row, col))

    def get_nodes(self, row, col, direction, count) -> List[InputNode]:
        result = []
        row_adj, col_adj = direction_adjustments[direction]
        for i in range(count):
            result.append(self.get(row + (row_adj * i), col + (col_adj * i)))
        return tuple(x for x in result if x is not None)

    @property
    def height(self):
        return self._max_row + 1

    @property
    def width(self):
        return self._max_col + 1


@dataclass(frozen=True)
class CombinedNode:
    orientation: str
    input_nodes: tuple[InputNode]

    @property
    def weight(self):
        return sum(x.weight for x in self.input_nodes)

    @property
    def first_input_node(self):
        return self.input_nodes[0]

    @property
    def last_input_node(self):
        return self.input_nodes[-1]


class CombinedNodeCollection:

    def __init__(self, nodes: List[CombinedNode]):
        self._dict: Dict[tuple, List] = {}
        for node in nodes:
            key = (node.first_input_node.row, node.first_input_node.col)
            if key not in self._dict:
                self._dict[key] = []
            self._dict[key].append(node)

    def __iter__(self) -> CombinedNode:
        for items in self._dict.values():
            for item in items:
                yield item

    def __len__(self):
        return sum(len(lst) for lst in self._dict.values())

    def find_by_first_node(self, row, col) -> List[CombinedNode]:
        result = self._dict.get((row, col), [])
        result.sort(key=lambda x: (len(x.input_nodes), x.input_nodes))
        return result

    def find_neighbors(self, combined_node: CombinedNode):
        last_input_node = combined_node.last_input_node
        if combined_node.orientation == 'h':
            desired_orientation = 'v'
            desired_rows = [last_input_node.row + 1, last_input_node.row - 1]
            desired_cols = [last_input_node.col]
        else:
            desired_orientation = 'h'
            desired_rows = [last_input_node.row]
            desired_cols = [last_input_node.col + 1, last_input_node.col - 1]
        result = []
        for row in desired_rows:
            for col in desired_cols:
                for candidate in self.find_by_first_node(row, col):
                    if candidate.orientation == desired_orientation:
                        if (last_input_node.row, last_input_node.col) not in [(x.row, x.col) for x in candidate.input_nodes]:
                            result.append(candidate)
        result.sort(key=lambda x: (len(x.input_nodes), x.input_nodes))
        return result


class GraphNode:
    def __init__(self, combined_node: CombinedNode = None):
        self.combined_node = combined_node
        self.neighbors: tuple[GraphNode] = tuple()
        self.distance = None
        self.visited = False
        self.previous = None

    def __repr__(self):
        return f"GraphNode(combined_node={self.combined_node}, visited={self.visited}, distance={self.distance}, neighbors={len(self.neighbors)})"


class Graph:

    def __init__(self, root: GraphNode):
        self._root = root
        self._nodes: Set[GraphNode] = set()
        queue = collections.deque()
        queue.append(root)
        while queue:
            node = queue.pop()
            if node not in self._nodes:
                self._nodes.add(node)
                queue.extend(node.neighbors)

    def __len__(self):
        return len(self._nodes)

    def __iter__(self) -> Iterator[GraphNode]:
        for node in self._nodes:
            yield node

    @property
    def root(self):
        return self._root

    def get_minimum_unvisited_node(self) -> GraphNode:
        result: GraphNode = None
        for node in self._nodes:
            if not node.visited and node.distance is not None:
                if result is None or result.distance > node.distance:
                    result = node
        return result


def main():
    global args
    args = argparser.parse_args()
    input_grid = get_input_grid()
    print(f"Input grid: {len(input_grid)}")
    combined_nodes = get_combined_nodes(input_grid)
    combined_node_collection = CombinedNodeCollection(combined_nodes)
    print(f"Combined nodes: {len(combined_node_collection)}")
    graph = build_graph(combined_node_collection)
    print(f"Graph: {len(graph)}")
    unvisited_nodes = [x for x in graph]
    current_node = get_node_with_min_distance(unvisited_nodes)
    nodes_visited = 0
    while current_node is not None:
        for neighbor in current_node.neighbors:
            if not neighbor.visited:
                distance = current_node.distance + neighbor.combined_node.weight
                if neighbor.distance is None or neighbor.distance > distance:
                    neighbor.distance = distance
                    neighbor.previous = current_node
        current_node.visited = True
        nodes_visited += 1
        if nodes_visited % 10000 == 0:
            print(nodes_visited, int(time.time() - start_time))
        current_node = get_node_with_min_distance(unvisited_nodes)
    terminal_nodes = find_terminal_nodes(graph, input_grid.height - 1, input_grid.width - 1)
    solution_node: GraphNode = None
    for terminal_node in terminal_nodes:
        if solution_node is None or solution_node.distance > terminal_node.distance:
            solution_node = terminal_node
    solution = solution_node.distance - input_grid.get(0, 0).weight
    print(solution)
    #print_path(solution_node, input_grid)
    #summarize_solution(solution_node, solution_node)


def get_node_with_min_distance(nodes: Set[GraphNode]) -> GraphNode:
    result: GraphNode = None
    for node in nodes:
        if node.distance is not None:
            if result is None or result.distance > node.distance:
                result = node
    if result is not None:
        nodes.remove(result)
    return result


def get_input_grid() -> InputGrid:
    result = InputGrid()
    for row, line in enumerate(get_lines()):
        for col, weight in enumerate(list(line)):
            result.add(InputNode(row, col, int(weight)))
    return result


def get_lines():
    with open(args.file) as file:
        for line in file:
            yield line.strip()


def get_combined_nodes(grid: InputGrid):
    temp: Set[CombinedNode] = set()
    for row in range(grid.height):
        for col in range(grid.width):
            for orientation in ['h', 'v']:
                for direction in ['e', 'w'] if orientation == 'h' else ['n', 's']:
                    for i in range(4, 11):
                        nodes = grid.get_nodes(row, col, direction, i)
                        if nodes and len(nodes) >= 4:
                            temp.add(CombinedNode(orientation, nodes))
    return [x for x in temp]


def build_graph(combined_node_collection: CombinedNodeCollection):
    mapping: Dict[CombinedNode, GraphNode] = {}
    for combined_node in combined_node_collection:
        graph_node = GraphNode(combined_node)
        mapping[combined_node] = graph_node
    for combined_node in combined_node_collection:
        graph_node = mapping[combined_node]
        neighbors = combined_node_collection.find_neighbors(combined_node)
        graph_node_neighbors = tuple([mapping[x] for x in neighbors])
        graph_node.neighbors = graph_node_neighbors
    root = GraphNode()
    root.neighbors = [mapping[x] for x in combined_node_collection.find_by_first_node(0, 0)]
    root.distance = 0
    return Graph(root)


def find_terminal_nodes(graph: Graph, last_row: int, last_col: int) -> List[GraphNode]:
    result = []
    for graph_node in graph:
        combined_node = graph_node.combined_node
        if combined_node and combined_node.last_input_node.row == last_row and combined_node.last_input_node.col == last_col:
            result.append(graph_node)
    return result


def print_grid(grid: InputGrid):
    for row in range(grid.height):
        for col in range(grid.width):
            node = grid.get(row, col)
            print(f"({node.row:>2}, {node.col:>2}, {node.weight:>2}) ", end='')
        print()


def print_path(solution_node: GraphNode, input_grid: InputGrid):
    print(solution_node.distance)
    path, graph_node = [], solution_node
    while graph_node is not None:
        if graph_node.combined_node:
            for input_node in reversed(graph_node.combined_node.input_nodes):
                path.append(input_node)
        graph_node = graph_node.previous
    path = set([(x.row, x.col) for x in path])
    for row in range(input_grid.height):
        for col in range(input_grid.width):
            if (row, col) in path:
                print('X', end='')
            else:
                print(input_grid.get(row, col).weight, end='')
        print()


def summarize_solution(solution_node: GraphNode, input_grid: InputGrid):
    graph_node = solution_node
    graph_nodes = []
    while graph_node is not None:
        graph_nodes.append(graph_node)
        graph_node = graph_node.previous
    combined_nodes = [x.combined_node for x in reversed(graph_nodes) if x.combined_node is not None]
    for node in combined_nodes:
        print(node.orientation)
        for x in node.input_nodes:
            print('\t', x)

if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
