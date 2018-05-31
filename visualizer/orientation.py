from enum import IntEnum


class Orientation(IntEnum):
    NORTH = -90
    EAST = 0
    SOUTH = 90
    WEST = 180

    def invert(self):
        return Orientation((self.value + 180) % 4)
