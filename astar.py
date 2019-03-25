#!/usr/bin/env python3

###
#   Trabalho Acadêmico Realizado para a disciplina de Sistemas Inteligentes,
#   do curso de Bach. em Sistemas de Informação na Universidade Técnológica
#   Federal do Paraná
#   Tema: Busca Heurística vs Busca Cega
#   Equipe:   Daniel Eduardo Vieira, 1366424
#           Saulo Silva, XXXXXX
#           Diego 'Foobar', XXXXXX
#   Prof.: Fabro
###

import numpy as np
from maze import Maze


class Node():
    """This class is used to represent the nodes in a path"""

    def __init__(self, position: list):
        self.position = position
        self.parent = None
        self.distfrom_source = -1
        self.heuristic = -1
        self.total_cost = -1
        return

    def __eq__(self, other):
        return self.position[0] == other.position[0] and \
            self.position[1] == other.position[1]


class UnwantedNode(Exception):
    """Exception raised if a node that would be appended
    is unwanted because is already appended on that list.

    Attributes:
        nd -- node involved
        lst -- list involved
        message -- explanation of the error
    """

    def __init__(self, nd: Node, lst: list):
        self.message = "Unable to add a node to this list"
        self.nd = str(nd)
        self.lst = str(lst)


def get_successors_coord(root: Node):
    return np.array([
        [root.position[0] + 0, root.position[1] - 1],
        [root.position[0] + 0, root.position[1] + 1],
        [root.position[0] - 1, root.position[1] + 0],
        [root.position[0] + 1, root.position[1] + 0],
        [root.position[0] - 1, root.position[1] - 1],
        [root.position[0] - 1, root.position[1] + 1],
        [root.position[0] + 1, root.position[1] - 1],
        [root.position[0] + 1, root.position[1] + 1]
    ],
        dtype=np.int32)


def get_successors(root: Node, matrix: np.ndarray):
    suc_coord = get_successors_coord(root)
    suc_list = list()
    for coord in suc_coord:
        if coord[0] >= 0 and \
            coord[0] < matrix.shape[0] and \
            coord[1] >= 0 and \
                coord[1] < matrix.shape[1] and \
                matrix[coord[0], coord[1]] != -2:

            node = Node(coord)
            node.parent = root
            if root:
                node.distfrom_source = root.distfrom_source + 1
            suc_list.append(node)

    return suc_list


def get_minor_cost(node_list: list):
    minor_cost = 0
    minor_index = 0
    for i in np.arange(0, len(node_list)):
        if minor_cost > node_list[i].total_cost:
            minor_cost = node_list[i].total_cost
            minor_index = i

    return node_list.pop(minor_index)


def euclidian_dist(coordA: list, coordB: list):
    # It's not needed to find the square root, because is crescent
    # and will not make difference in this result
    return (coordA[0] - coordB[0]) ** 2 + (coordA[1] - coordB[1]) ** 2


def astar(matrix: np.ndarray, source: list, target: list):
    """Returns a list of tuples as a path from the given
    start to the given end in the given maze
    maze: Maze object used as environment
    source: [x,y] coordinates of source position
    target: [x,y] coordinates of target position
    """
    nodes_open = list()
    nodes_closed = list()

    # Append the source node to the open list
    src = Node(source)
    src.distfrom_source = 0
    src.total_cost = 0
    src.heuristic = euclidian_dist(source, target)
    nodes_open.append(src)

    # Create the target node for comparison
    target_node = Node(target)

    while nodes_open:
        minor = get_minor_cost(nodes_open)
        successors = get_successors(minor, matrix)

        for successor in successors:
            successor.heuristic = \
                euclidian_dist(successor.position, target)

            successor.total_cost = \
                successor.distfrom_source + successor.heuristic

            if successor.__eq__(target_node):
                it = successor
                path = list()

                while it.parent:
                    path.append([it.position])
                    it = it.parent

                return path[::-1]

            if successor in nodes_closed:
                continue

            try:
                for i, node in enumerate(nodes_open):
                    if successor.__eq__(node):
                        if successor.total_cost < node.total_cost:
                            nodes_open.pop(i)
                            break
                        else:
                            raise UnwantedNode(successor, nodes_open)
            except UnwantedNode:
                continue

            nodes_open.append(successor)

        nodes_closed.append(minor)

    return None


if __name__ == '__main__':
    # Showing off usage
    side_size = np.random.randint(10, 50)
    source = [np.random.randint(0, side_size), np.random.randint(0, side_size)]
    target = [np.random.randint(0, side_size), np.random.randint(0, side_size)]
    maze = Maze(side_size, source, target, blocked_area=0.6)
    path = astar(maze.matrix, source, target)

    if path:
        print("Search finished: Path Found")
        # Uncomment the line below to get an visual output
        # maze.print_maze(path=path)
    else:
        print("Search finished: No path from source to target available.")
