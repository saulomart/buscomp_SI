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
import pandas as pd
from random import randint

#   Values in the matrix represents the status of that
#   position, accord to the info below:
#   Target Position == -3
#   Blocked Space == -2
#   Unused Space == -1
#   Source Position == 0
#   Unblocked Space > 0


class Maze(pd.DataFrame):
    def __init__(self, lines: np.int8, collumns: np.int8):
        # Generating empty matrix then filling with -1
        # It's faster than use np.full
        matrix = np.empty((lines, collumns), dtype=np.int8)
        matrix.fill(-1)

        # This class behave just like an DataFrame
        super(Maze, self).__init__(matrix, dtype=np.int8)
        return

    def generate(self,
                 source_posX: np.int8, source_posY: np.int8,
                 target_posX: np.int8, target_posY: np.int8,
                 all_paths=False):
        """
        :param source_posX: TO DO
        :all_paths: Generate an auxiliar representation of the maze in csv with all costs for visualization
        """
        # Getting the shape of this DataFrame
        lines = self.shape[0]
        collumns = self.shape[1]

        # Setting the value of each node with the following value:
        # Distance between source and a node + Distance between this
        # node and the target
        self.iat[source_posX, source_posY] = 0
        self.iat[target_posX, target_posY] = -3

        distfrom_source = 1
        total_of_items = lines * collumns
        unblocked = 2
        blocked = 0

        # Blocking randomly positions
        for i in np.arange(0, lines):
            for j in np.arange(0, collumns):
                if randint(0, 6) > 5 and self.iat[i, j] == -1:
                    self.iat[i, j] = -2
                    blocked += 1

        self.to_csv(path_or_buf='maze.csv', index=False, header=False)

        if all_paths:
            # Filling the unblocked spaces
            while unblocked + blocked < total_of_items:
                for i in np.arange(source_posX - distfrom_source,
                                   source_posX + distfrom_source + 1):
                    for j in np.arange(source_posY - distfrom_source,
                                       source_posY + distfrom_source + 1):
                        if i < lines and j < collumns and i >= 0 and j >= 0:
                            if self.iat[i, j] == -1:
                                if np.abs(i - target_posX) > \
                                        np.abs(j - target_posY):
                                    distfrom_end = np.abs(i - target_posX)
                                else:
                                    distfrom_end = np.abs(j - target_posY)

                                self.iat[i, j] = distfrom_source + distfrom_end
                                unblocked += 1
                        j += 1
                    i += 1
                distfrom_source += 1

            self.to_csv(path_or_buf='maze_all_path.csv',
                        index=False, header=False)
