import typing
from enum import Enum
import random

from attr import dataclass


@dataclass(frozen=True)
class Location:
    row: int
    column: int

class CellType(Enum):
    """
    # Cell
    - class representing a cell
    """
    EMPTY = '_'
    OBSTACLE = '#'
    START = 'S'
    GOAL = 'G'
    PATH = '*'
    DEBUG = '?'


class Labyrinth:
    def __init__(self, rows: int, cols: int, spread: float, start: Location, goal: Location) -> None:
        """spread: float between 0 and 1 -> percent of cells that will be obstacles"""
        self.__rows = rows
        self.__cols = cols
        self.__spread = spread

        self.__start = start
        self.__goal = goal

        # setup grid
        self.__grid = [[ CellType.EMPTY for _ in range(cols) ] for _ in range(rows) ]

        self.__fill_with_obstacles()
        pass

    def __fill_with_obstacles(self):
        for r in self.__grid:
            for i in range(self.__cols):
                if random.random() < self.__spread:
                    r[i] = CellType.OBSTACLE

        self.__grid[self.__start.row][self.__start.column] = CellType.START
        self.__grid[self.__goal.row][self.__goal.column] = CellType.GOAL

    def __str__(self) -> str:
        result = ""
        for r in self.__grid:
            for c in r:
                result += c.value
            result += "\n"
        return result

    def get_neighbors(self, location: Location) -> list[Location]:
        neighbors = []

        def check_location(row: int, col: int) -> bool:
            return 0 <= row < self.__rows and 0 <= col < self.__cols and self.__grid[row][col] != CellType.OBSTACLE

        if check_location(location.row, location.column - 1):
            neighbors.append(Location(location.row, location.column - 1))

        if check_location(location.row, location.column + 1):
            neighbors.append(Location(location.row, location.column + 1))

        if check_location(location.row - 1, location.column):
            neighbors.append(Location(location.row - 1, location.column))

        if check_location(location.row + 1, location.column):
            neighbors.append(Location(location.row + 1, location.column))
        return neighbors


class Node:
    def __init__(self, state: int, parent: typing.Self = None):
        self.state = state
        self.parent = parent

    def __repr__(self) -> str:
        return str(self.state)




class Stack[T]:
    def __init__(self):
        self.__container: list[T] = []

    def pop(self) -> T:
        return self.__container.pop()

    def push(self, value: T):
        self.__container.append(value)

    def __contains__(self, item: T) -> bool:
        return self.__container.__contains__(item)

    def __len__(self) -> int:
        return self.__container.__len__()

    def is_empty(self) -> bool:
        return self.__container.__len__() == 0

    def __repr__(self) -> str:
        return self.__container.__repr__()

