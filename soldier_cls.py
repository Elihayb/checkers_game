from types_cls import Types


class Soldier:
    def __init__(self, color):
        if color != Types.BLACK and color != Types.WHITE:
            raise ValueError("Invalid square color, Must be WHITE or BLACK")
        self.color = color
        self.is_king = False
        self.x = None
        self.y = None

    def get_location(self):
        if self.x is None or self.y is None:
            raise ValueError("Location was not initialized")
        return self.x, self.y

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.color},{self.is_king = }"
