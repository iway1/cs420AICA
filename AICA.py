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
        self.cells = self.random_cells()
        self.updated = None

    def random_cells(self):
        from random import randint
        cells = []
        for i in range(self.N):
            new_row = []
            for _ in range(self.N):
                new_element = randint(0, 1)
                if new_element == 0:
                    new_element = -1
                new_row.append(new_element)
            cells.append(new_row)
        return numpy.array(cells)

    def random_cell_coords(self):
        # Returns the row and column of a random un-updated cell.
        from random import randint
        r = randint(0, self.N - 1)
        c = randint(0, self.N - 1)
        while self.updated[r, c]: #Find unupdated cell by searching left-to-right top to bottom, wrapping at the bottom.
            if c == self.N - 1:
                r = (r + 1) % self.N
                c = 0
            else:
                c += 1
        return r, c

    def update_cell(self, r, c):
        pass

    def update_cells(self):
        self.updated = numpy.zeros([self.N, self.N])
        n_updated = 0
        for _ in range(self.N**2):
            self.update_cell(*self.random_cell_coords())
        self.assert_finished_update()

    def assert_finished_update(self):
        assert not (0 in self.updated.unique()), "Not all cells were updated."

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