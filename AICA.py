__author__ = 'iway1'

import numpy


class AICA:
    def __init__(self, experiment_id, N, J1, J2, h, R1, R2):
        self.id = experiment_id
        self.J1 = J1
        self.J2 = J2
        self.h = h
        self.R1 = R1
        self.R2 = R2
        self.N = N
        self.init_cells()
    def init_cells(self):
        from random import randint
        self.cells = []
        for i in range(self.N):
            new_row = []
            for _ in range(self.N):
                new_element = randint(0, 1)
                if new_element == 0:
                    new_element = -1
                new_row.append(new_element)
            self.cells.append(new_row)
        self.cells = numpy.array(self.cells)

    def distance(self, cell_1, cell_2):
        dist_y = abs(cell_1[0] - cell_2[0])
        dist_x = abs(cell_1[1] - cell_2[1])
        if dist_y > self.N // 2:
            dist_y = self.N - dist_y
        if dist_x > self.N // 2:
            dist_x = self.N - dist_x
        return dist_y + dist_x

    def __getitem__(self, item):
        if type(item) != tuple or len(item) != 2:
            raise ValueError("Pass a tuple of length two to get item!")
        return self.cells[item]
    def __setitem__(self, key, value):
        if type(value) != int:
            raise ValueError("Only int values may be assigned to a cell.")
        if value != -1 and value != 1:
            raise ValueError("Cells may only take a value on of +/- 1.")
        self.cells[key] = value
    def __str__(self):
        return str(self.cells)

if __name__ == '__main__':
    ca = AICA("none", 30, None, None, None, None, None)