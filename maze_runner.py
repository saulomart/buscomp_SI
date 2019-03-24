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

# Values in matrix represents the status of the position
# 


class Maze(pd.DataFrame):
    def __init__(self, lines: np.int16, collumns: np.int16):
        # Generating empty matrix then filling with -1
        # It's faster than use np.full
        matrix = np.empty((lines, collumns), dtype=np.int16)
        matrix.fill(-1)

        # This class behave just like an DataFrame
        super(Maze, self).__init__(matrix, dtype=np.int16)
        return

    def trace_route(self,
                    start_posX: np.int16, start_posY: np.int16,
                    destination_posX: np.int16, destination_posY: np.int16):
        # Getting the shape of this DataFrame
        lines = self.shape[0]
        collumns = self.shape[1]

        # Setting the distance between the start position and all nodes
        self.iat[start_posX, start_posY] = 0

        distfrom_start = 1
        total_of_items = lines * collumns
        iterated_items = 1

        while iterated_items < total_of_items:
            for i in np.arange(start_posX - distfrom_start,
                               start_posX + distfrom_start + 1):
                for j in np.arange(start_posY - distfrom_start,
                                   start_posY + distfrom_start + 1):
                    if i < lines and j < collumns and i >= 0 and j >= 0:
                        if self.iat[i, j] == -1:
                            if np.abs(i - destination_posX) > \
                                np.abs(j - destination_posY):
                                distfrom_end = np.abs(i - destination_posX)
                            else:
                                distfrom_end = np.abs(j - destination_posY)

                            self.iat[i, j] = distfrom_start + distfrom_end
                            iterated_items += 1
                    j += 1
                i += 1
            distfrom_start += 1

        # Calculating the best route


if __name__ == '__main__':
    teste = Maze(10, 10)
    teste.trace_route(2, 2, 9, 9)
    print(teste.to_string(index=False, header=False, col_space=3))
