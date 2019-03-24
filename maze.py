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


class Maze():
    def __init__(self, side_size: np.int32, source:list, target:list, blocked_area=0.2):
        """Creates an empty Maze with an matrix representing its paths, the paths are generated randomly

        blocked_area: percentage of total area there will be blocked, the positions chosen are random"""
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
            for p in path:
                if self.matrix[tuple(p[0])] == -1:
                    self.matrix[tuple(p[0])] = -4

        for i in np.arange(0, self.matrix.shape[0], dtype=np.int32):
            for j in np.arange(0, self.matrix.shape[1], dtype=np.int32):
                if self.matrix[i, j] == -2:
                    print("+", end=' ')
                elif self.matrix[i, j] == 0:
                    print("@", end=' ')
                elif self.matrix[i, j] == -3:
                    print("?", end=' ')
                elif self.matrix[i, j] == -4:
                    print("o", end=' ')
                else:
                    print(".", end=' ')
            print("")
