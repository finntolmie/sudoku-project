import pygame


class Cell:

    def __init__(self, row, col, colour, val):
        self.row = row
        self.col = col
        self.colour = colour
        self.val = val

    def change_value(self, val):
        self.val = val

    def copy(self):
        return Cell(self.row, self.col, self.val)
