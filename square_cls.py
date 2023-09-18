from soldier_cls import Soldier
from types_cls import Types


class Square:
    def __init__(self, color):
        if color != Types.BLACK and color != Types.WHITE:
            raise ValueError("Invalid square color, Must be WHITE or BLACK")
        self.color = color
        self._soldier = None
        self.x = None
        self.y = None

    @property
    def soldier(self):
        return self._soldier

    @soldier.setter
    def soldier(self, value):
        self._soldier = value
        self._soldier.set_location(self.x, self.y)

    def remove_soldier(self):
        self._soldier = None

    def get_location(self):
        if self.x is None or self.y is None:
            raise ValueError("Location was not initialized")
        return self.x, self.y

    def set_location(self, x, y):
        if self.x is not None or self.y is not None:
            raise ValueError("Location of square cannot be defined")
        self.x = x
        self.y = y

    def __repr__(self):
        string = f'Square color {self.color}'
        if isinstance(self.soldier, Soldier):
            string += f', soldier {self.soldier}'
        else:
            string += ', Soldier = None'
        string += " | "
        return string
