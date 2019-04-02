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


class PositionException(Exception):
    def __init__(self):
        self.msg = "Unable to find this position"


class Position():
    """
        N.W---N----N.E

        W----Cell----E

        S.W---S----S.E

        6 - N -->  North
        5 - N.E--> North-East
        4 - E -->  East
        3 - S.E--> South-East
        2 - S -->  South
        1 - S.W--> South-West
        0 - W -->  West
        7 - N.W--> North-West

        def translateDirection(p: int):
            if (p == 0):
                return 'W'
            elif (p == 1):
                return 'SW'
            elif (p == 2):
                return 'S'
            elif (p == 3):
                return 'SE'
            elif (p == 4):
                return 'E'
            elif (p == 5):
                return 'NE'
            elif (p == 6):
                return 'N'
            elif (p == 7):
                return 'NW'

            return None
    """

    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.direction = direction

    def __eq__(self, other):
        return self.x == other.x and \
            self.y == other.y and \
            self.direction == other.direction

    def getFoward(self):
        if (self.direction == 0):
            return Position(self.x, self.y - 1, self.direction)
        elif (self.direction == 1):
            return Position(self.x + 1, self.y - 1, self.direction)
        elif (self.direction == 2):
            return Position(self.x + 1, self.y, self.direction)
        elif (self.direction == 3):
            return Position(self.x + 1, self.y + 1, self.direction)
        elif (self.direction == 4):
            return Position(self.x, self.y + 1, self.direction)
        elif (self.direction == 5):
            return Position(self.x - 1, self.y + 1, self.direction)
        elif (self.direction == 6):
            return Position(self.x - 1, self.y, self.direction)
        elif (self.direction == 7):
            return Position(self.x - 1, self.y - 1, self.direction)
        else:
            raise PositionException()

    def getRight(self):
        if (self.direction == 0):
            return Position(self.x, self.y, 7)
        else:
            return Position(self.x, self.y, self.direction - 1)

    def getLeft(self):
        if (self.direction == 7):
            return Position(self.x, self.y, 0)
        else:
            return Position(self.x, self.y, self.direction + 1)

    def turnRight(self):
        if (self.direction == 0):
            self.direction = 7
        else:
            self.direction -= 1
        return

    def turnLeft(self):
        if (self.direction == 7):
            self.direction = 0
        else:
            self.direction += 1
        return

    def moveFoward(self):
        if (self.direction == 0):
            self.y -= 1
        elif (self.direction == 1):
            self.x += 1
            self.y -= 1
        elif (self.direction == 2):
            self.x += 1
        elif (self.direction == 3):
            self.x += 1
            self.y += 1
        elif (self.direction == 4):
            self.y += 1
        elif (self.direction == 5):
            self.x -= 1
            self.y += 1
        elif (self.direction == 6):
            self.x -= 1
        elif (self.direction == 7):
            self.x -= 1
            self.y -= 1
        else:
            raise PositionException()
        return


class Node():
    """This class is used to represent the nodes in a path"""

    def __init__(self, position: Position):
        self.position = position
        self.parent = None
        self.distfrom_source = -1
        self.heuristic = -1
        self.total_cost = -1
        return

    def __eq__(self, other):
        return self.position.__eq__(other.position)


class UnwantedNode(Exception):
    """Exception raised if a node that would be appended
    is unwanted because is already appended on that list.

    Attributes:
        nd -- node involved
        lst -- list involved
        message -- explanation of the error
    """

    def __init__(self):
        self.message = "Unable to add a node to this list"
        # self.nd = str(nd)
        # self.lst = str(lst)
        return


def get_successors_pos(root: Node):
    return [root.position.getLeft(),
            root.position.getRight(),
            root.position.getFoward()]


def get_successors(root: Node, matrix: np.ndarray):
    suc_pos = get_successors_pos(root)
    suc_list = list()
    for pos in suc_pos:
        if pos.x >= 0 and \
            pos.x < matrix.shape[0] and \
            pos.y >= 0 and \
                pos.y < matrix.shape[1] and \
                matrix[pos.x, pos.y] != -2:

            node = Node(pos)
            node.parent = root

            if root:
                if root.position.x == node.position.x and \
                        root.position.y == node.position.y and \
                        root.position.direction == node.position.direction:
                    node.distfrom_source = root.distfrom_source + 1
                else:
                    node.distfrom_source = root.distfrom_source

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


def euclidian_dist(coordA: Position, coordB: Position):
    # It's not needed to find the square root, because is crescent
    # and will not make difference in this result
    return (coordA.x - coordB.x) ** 2 + (coordA.y - coordB.y) ** 2


def astar(matrix: np.ndarray, source: Position, target: Position):
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

    while nodes_open:
        minor = get_minor_cost(nodes_open)
        successors = get_successors(minor, matrix)

        for successor in successors:
            successor.heuristic = \
                euclidian_dist(successor.position, target)

            successor.total_cost = \
                successor.distfrom_source + successor.heuristic

            if euclidian_dist(successor.position, target) == 0:
                it = successor
                path = list()

                while it.parent:
                    path.append([it.position.x,
                                 it.position.y,
                                 it.position.direction])
                    it = it.parent

                return path[::-1]

            try:
                for i, node in enumerate(nodes_closed):
                    if successor.__eq__(node):
                        raise UnwantedNode()
            except UnwantedNode:
                continue

            try:
                for i, node in enumerate(nodes_open):
                    if successor.__eq__(node):
                        if successor.total_cost < node.total_cost:
                            nodes_open.pop(i)
                            break
                        else:
                            raise UnwantedNode()
            except UnwantedNode:
                continue

            nodes_open.append(successor)

        nodes_closed.append(minor)

    return None


if __name__ == '__main__':
    # Showing off usage
    print('Insira os dados da busca:\n')
    side_size = np.int32(input('\tTamanho do lado do labirinto: '))
    # np.random.randint(10, 50)

    source = Position(np.int32(input('\tCoordenada X do agente: ')),
                      np.int32(input('\tCoordenada Y do agente: ')),
                      np.random.randint(0, 8, dtype=np.int8))

    target = Position(np.int32(input('\tCoordenada X do destino: ')),
                      np.int32(input('\tCoordenada Y do destino: ')),
                      np.random.randint(0, 8, dtype=np.int8))

    print('\n\tAgora só falta definir o percentual máximo de caminhos',
          '\n\tbloqueados possíveis, pode ser qualquer valor positivo ou',
          '\n\tzero. Esse valor é um multiplicador que será usado para',
          '\n\tgerar os bloqueios randomicamente, junto com o labirinto,',
          '\n\tpor isso não é recomendado um número maior que 0.6 caso',
          '\n\tseja desejado que exista pelo menos um caminho disponível')

    maze = Maze(side_size,
                [source.x, source.y],
                [target.x, target.y],
                np.float(input('\n\t> Valor do multiplicador: ')))

    path = astar(maze.matrix, source, target)

    if path:
        print("\nSearch finished: Path Found")
        # Comment the line below to toggle off the fancy visual output. (faster)
        maze.print_maze(path=path)
    else:
        print("\nSearch finished: No path from source to target available.")
