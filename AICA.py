__author__ = 'iway1'




class AICA:
    def __init__(self, experiment_id, J1, J2, h, R1, R2):
        self.id = experiment_id
        self.J1 = J1
        self.J2 = J2
        self.h = h
        self.R1 = R1
        self.R2 = R2
    def init_cells(self):
        