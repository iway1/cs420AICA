__author__ = 'iway1'

import numpy
from bs4 import BeautifulSoup
colors = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255)
}

DEFAULT_IMAGE_SIZE = (120, 120)

class AICAExperiment:
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
        self.soup = BeautifulSoup("<body></body>","html.parser")
        self.images = []

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

    def iter_cells(self):
        for r in range(self.N):
            for c in range(self.N):
                yield r, c


    def update_cell(self, r, c):
        near_sum = 0
        far_sum = 0
        for check_row, check_col in self.iter_cells():
            dist = self.distance((r, c), (check_row, check_col))
            if dist < self.R2:
                if dist >= self.R1:
                    # Add to far sum
                    far_sum += self[check_row, check_col]
                else:
                    # Add to near sum
                    near_sum += self[check_row, check_col]
        near_sum *= self.J1
        far_sum *=  self.J2
        final = near_sum + far_sum + self.h
        if final >= 0:
            self[r, c] = 1
        else:
            self[r, c] = -1
        self.updated[r, c] = 1

    def update_cells(self):
        self.updated = numpy.zeros([self.N, self.N])
        n_updated = 0
        for _ in range(self.N**2):
            self.update_cell(*self.random_cell_coords())
        self.assert_finished_update()

    def assert_finished_update(self):
        assert not (0 in numpy.unique(self.updated)), "Not all cells were updated."

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

    def get_image(self, size=DEFAULT_IMAGE_SIZE):
        from PIL import Image
        rows = []
        for r in range(self.N):
            new_row = []
            for c in range(self.N):
                if self[r, c] == 1:
                    new_row.append(colors['WHITE'])
                elif self[r, c] == -1:
                    new_row.append(colors['BLACK'])
                else:
                    raise ValueError("Found bad value at cell {} {}: {}, couldn't create image.".format(r, c, self[r, c]))
            rows.append(new_row)
        return Image.fromarray(numpy.array(rows, dtype='uint8'), 'RGB')

    def show_image(self, size=DEFAULT_IMAGE_SIZE):
        im = self.get_image()
        im = im.resize(size)
        im.show()

    def save_image(self, name, size=DEFAULT_IMAGE_SIZE):
        import os
        from PIL import ImageOps
        im = self.get_image()
        im = im.resize(size)

        im = ImageOps.expand(im, border=8, fill='grey')
        im = ImageOps.expand(im, border=1, fill='black')

        if not os.path.isdir("images/" + self.id):
            os.mkdir("images/" + self.id)
        im_str = "images/" + self.id + "/" + name + ".jpg"
        im.save(im_str)
        image_tag = self.soup.new_tag("img", src="../" + im_str)
        self.soup.body.append(image_tag)

    def save_gif(self):

    def iterate(self):
        self.update_cells()
        self.images.append()

    def iterate_and_save(self, n, verbose=1):
        if verbose: print("Starting iterating and saving.")

        for i in range(n):
            if verbose: print("Update iteration {}.".format(i))
            self.update_cells()
            self.save_image("img{}".format(i))
            if verbose: print("Saved.")
        if verbose: print("Saving html.")
        self.save_html()



if __name__ == '__main__':
    experiment = AICAExperiment("test_experiment", 30, 1., -.1, 0, 6, 2)



    experiment.iterate_and_save(2)
