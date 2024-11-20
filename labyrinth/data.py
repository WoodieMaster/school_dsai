import typing
from collections import deque
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import Enum
import random

import pygame
from pygame import Surface
from pygame.display import set_gamma_ramp


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

class SearchState:
    def __init__(self):
        self.frontiers = deque[Node]()
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

    def draw(self, screen: Surface, search_state: SearchState) -> None:
        cell_height = screen.get_height() / self.__rows
        cell_width = screen.get_width() / self.__cols
        inset = .1
        if search_state.result is None:
            return
        for row_idx, cols in enumerate(self.__grid):
            for col_idx, cell in enumerate(cols):
                start_pos_x = col_idx * cell_width + cell_width * inset
                start_pos_y = row_idx * cell_height + cell_height * inset

                draw_width = cell_width * (1 - (inset * 2))
                draw_height = cell_height * (1 - (inset * 2))

                color = None
                if cell == CellType.OBSTACLE:
                    color = (90, 90, 90)
                elif cell == CellType.START:
                    color = (255, 0, 255)
                elif cell == CellType.GOAL:
                    color = (0, 255, 255)
                else:
                    pos = Location(row_idx, col_idx)
                    result_path = set[Location]()
                    if search_state.result is not None:
                        node = search_state.result
                        while node.parent is not None:
                            result_path.add(node.location)
                            node = node.parent

                    if pos in result_path:
                        color = (0,255,0)
                    elif pos in search_state.visited_locations:
                        color = (255, 0, 0)
                    elif pos in search_state.frontier_locations:
                        color = (255, 255, 0)
                if color is not None:
                    pygame.draw.rect(screen, color, (start_pos_x, start_pos_y, draw_width, draw_height))

        pygame.display.flip()

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

    # def colored_print(self, visited: set[Location], new_locations: set[Location]):
    #     os.system("cls")
    #     for row_idx, cols in enumerate(self.__grid):
    #         for col_idx, cell in enumerate(cols):
    #             if Location(row_idx, col_idx) in visited:
    #                 print("\033[41m" + cell.value + "\033[0m", end="")
    #             elif Location(row_idx, col_idx) in new_locations:
    #                 print("\033[43m" + cell.value + "\033[0m", end="")
    #             else:
    #                 print(cell.value, end="")
    #         print("\n", end="")
    #
    # def final_print(self, target_node: Node):
    #     os.system("cls")
    #     colored_nodes = set[Location]()
    #     while target_node is not None:
    #         colored_nodes.add(target_node.location)
    #         target_node = target_node.parent
    #
    #     for row_idx, cols in enumerate(self.__grid):
    #         for col_idx, cell in enumerate(cols):
    #             if Location(row_idx, col_idx) in colored_nodes:
    #                 print("\033[42m" + cell.value + "\033[0m", end="")
    #             else:
    #                 print(cell.value, end="")
    #         print("\n", end="")


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

class Stack[T]:
    def __init__(self):
        self.__container: list[T] = []

    def pop(self) -> T:
        return self.__container.pop()

    def push(self, value: T):
        self.__container.append(value)

    def shift(self, value: T):
        self.__container.insert(0, value)

    def append(self, other: Iterable[T]):
        for el in other:
            self.__container.append(el)

    def __contains__(self, item: T) -> bool:
        return self.__container.__contains__(item)

    def __len__(self) -> int:
        return self.__container.__len__()

    def is_empty(self) -> bool:
        return self.__container.__len__() == 0

    def __repr__(self) -> str:
        return self.__container.__repr__()

    def __iter__(self) -> Iterator[T]:
        return self.__container.__iter__()

