#!/usr/bin/env python3

###
#   Trabalho Acadêmico Realizado para a disciplina de Sistemas Inteligentes,
#   do curso de Bach. em Sistemas de Informação na Universidade Técnológica
#   Federal do Paraná
#   Tema: Busca Heurística vs Busca Cega
#   Equipe:   Daniel Eduardo Vieira, 1366424
#           Saulo Silva, XXXXXX
#           Diego Mamprim, 1937537
#   Prof.: Fabro
###

import numpy as np


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


class Maze():
    """
    Creates an empty Maze with an matrix representing its paths, the paths are generated randomly.

    : param blocked_area: multiplicator used to get a number of blocked areas where 0 is none blocked area and 1 is a lot. format: [0, 1)


    Labels:

    Blocked: -2 | char: '+' \n
    Unblocked: -1 | char: '.' \n
    Source: 0 | char: '@' \n
    Target: -3 | char: '?' \n
    Path: -4 | char: 'o' \n
    """

    def __init__(self, side_size: np.int32, source: list, target: list, blocked_area=0.2):
        # Generating empty matrix then filling with -1
        # It's faster than use np.full
        self.matrix = np.empty([side_size, side_size], dtype=np.int32)
        self.matrix.fill(-1)

        # Blocking randomly positions
        number_of_blocks = np.int32(
            self.matrix.shape[0] * self.matrix.shape[1] * blocked_area)
        blockedX = np.random.randint(
            0, self.matrix.shape[0], size=number_of_blocks, dtype=np.int32)
        blockedY = np.random.randint(
            0, self.matrix.shape[1], size=number_of_blocks, dtype=np.int32)

        self.matrix[blockedX, blockedY] = -2

        self.matrix[source[0], source[1]] = 0
        self.matrix[target[0], target[1]] = -3

        return

    def print_maze(self, path=[]):
        if path:
            print("Path ( Step [x, y, direction] ):")
            for i, p in enumerate(path):
                print('\t', i, p, translateDirection(p[2]))
                tpl = tuple([p[0], p[1]])
                if self.matrix[tpl] == -1:
                    self.matrix[tpl] = -4

        print("\n###\tMAZE\t###")
        for i in np.arange(0, self.matrix.shape[0], dtype=np.int32):
            for j in np.arange(0, self.matrix.shape[1], dtype=np.int32):
                if self.matrix[i, j] == -2:
                    print(".", end=' ')
                elif self.matrix[i, j] == 0:
                    print("S", end=' ')
                elif self.matrix[i, j] == -3:
                    print("T", end=' ')
                elif self.matrix[i, j] == -4:
                    print("o", end=' ')
                else:
                    print(" ", end=' ')
            print("")

        print('\nLabels:\n\tS -- Source\n\tT -- TARGET\n\to -- PATH\n\t. -- BLOCKED WAY')
