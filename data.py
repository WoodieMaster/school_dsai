import random
import typing
from abc import abstractmethod
from collections import deque
from dataclasses import dataclass
from enum import Enum
import heapq
from logging import lastResort

import pygame
from pygame import Surface

background_colour = (0,0,0)
def clear_window(screen: Surface):
    screen.fill(background_colour)

@dataclass(frozen=True)
class Location:
    row: int
    column: int

class CellType(Enum):
    """
    # Cell
    - class representing a cell
    """
    EMPTY = ' '
    OBSTACLE = '■'
    START = 'S'
    GOAL = 'G'
    PATH = '*'
    DEBUG = '?'

class Node:
    def __init__(self, location: Location, parent: typing.Self = None):
        self.location = location
        self.parent = parent

    def __repr__(self) -> str:
        return str(self.location)

    def __lt__(self, other: typing.Self) -> bool:
        return True

class FrontierWrapper:
    def __init__(self):
        pass

    @abstractmethod
    def push(self, value: Node):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

class NodeQueue(FrontierWrapper):
    def __init__(self):
        super().__init__()
        self.__container = deque[Node]()

    def push(self, value: Node):
        self.__container.append(value)

    def pop(self) -> Node:
        return self.__container.popleft()

    def __len__(self):
        return self.__container.__len__()

def calculate_cost(a: Location, b: Location) -> int:
    return abs(a.row - b.row) + abs(a.column - b.column)

class NodePrioQueue(FrontierWrapper):
    def __init__(self, target: Location):
        super().__init__()
        self.__target = target
        self.__step_count = 0
        self.__container: list[tuple[int, Node, int]] = []

    def push(self, value: Node):
        step_count = self.__step_count + 1
        cost = calculate_cost(value.location, self.__target) + step_count
        heapq.heappush(self.__container, (cost, value, step_count))

    def pop(self) -> Node:
        cost, node, step_count = heapq.heappop(self.__container)
        self.__step_count = step_count
        return node

    def __len__(self):
        return self.__container.__len__()

class NodeStack(FrontierWrapper):
    def __init__(self):
        super().__init__()
        self.__container = list[Node]()

    def push(self, value: Node):
        self.__container.append(value)

    def pop(self) -> Node:
        return self.__container.pop()

    def __len__(self):
        return self.__container.__len__()

class SearchState:
    def __init__(self, frontier: FrontierWrapper):
        self.frontiers = frontier
        self.visited_locations = set[Location]()
        self.result: Node | None = None
        self.frontier_locations = set[Node]()


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

    def rows(self) -> int:
        return self.__rows

    def cols(self) -> int:
        return self.__cols

    def grid_items(self) -> enumerate[list[CellType]]:
        return enumerate(self.__grid)

    def goal(self) -> Location:
        return self.__goal

    def __fill_with_obstacles(self):
        for r in self.__grid:
            for i in range(self.__cols):
                if random.random() < self.__spread:
                    r[i] = CellType.OBSTACLE

        self.__grid[self.__start.row][self.__start.column] = CellType.START
        self.__grid[self.__goal.row][self.__goal.column] = CellType.GOAL

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

    def get_state(self, location: Location) -> CellType:
        return self.__grid[location.row][location.column]
