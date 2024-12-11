from collections.abc import Callable, Generator

import pygame
from pygame import Surface

import algorithms
from labyrinth.data import Location, Labyrinth, Node, clear_window, SearchState, CellType

pygame.init()

LAB_ROWS = 190
LAB_COLS = 300
SCALE = 3
START = Location(LAB_ROWS // 2, LAB_COLS // 2)


type Algorithm = Callable[[Labyrinth, Node], Generator[algorithms.SearchState, None, None]]

algorithm_list: list[tuple[Algorithm,str]] = [
    (algorithms.breadth_first_search, "Breadth First Search"),
    (algorithms.depth_first_search, "Depth First Search"),
    (algorithms.a_star_search, "A Star Search"),
]

def create_window() -> Surface:
    screen = pygame.display.set_mode((LAB_COLS * SCALE, LAB_ROWS * SCALE))

    pygame.display.set_caption('Search Algorithms')

    clear_window(screen)

    return screen


class Program:
    def __init__(self, screen: Surface):
        self.algorithm: Algorithm | None = None
        self.labyrinth: Labyrinth | None = None
        self.screen = screen

    def draw_labyrinth(self, search_state: SearchState | None) -> None:
        clear_window(self.screen)
        cell_height = self.screen.get_height() / self.labyrinth.rows()
        cell_width = (self.screen.get_width() / self.labyrinth.cols())
        inset = .1

        result_path = set[Location]()
        if search_state is not None and search_state.result is not None:
            node = search_state.result
            while node.parent is not None:
                result_path.add(node.location)
                node = node.parent

        for row_idx, cols in self.labyrinth.grid_items():
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
                elif search_state is not None:
                    pos = Location(row_idx, col_idx)

                    if pos in result_path:
                        color = (0, 255, 0)
                    elif pos in search_state.visited_locations:
                        color = (255, 0, 0)
                    elif pos in search_state.frontier_locations:
                        color = (255, 255, 0)
                if color is not None:
                    pygame.draw.rect(self.screen, color, (start_pos_x, start_pos_y, draw_width, draw_height))

        pygame.display.flip()

    def select_algorithm(self, idx: int):
        if self.labyrinth is None:
            self.labyrinth = create_labyrinth(LAB_ROWS, LAB_COLS)
        algorithm_idx = idx
        if algorithm_idx >= len(algorithm_list) or algorithm_idx < 0:
            print(f"Invalid algorithm index {algorithm_idx}! Max index: {len(algorithm_list)}")
            return
        algorithm, name = algorithm_list[algorithm_idx]
        self.algorithm = algorithm
        pygame.display.set_caption('Search Algorithms - ' + name)

    def handle_event(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)

            if event.type == pygame.KEYDOWN:
                # No normal character
                if len(event.unicode) != 1:
                    continue

                # Select algorithm by digit
                if ord(event.unicode) in range(ord('1'), ord('9') + 1):
                    self.select_algorithm(ord(event.unicode) - ord('1'))
                    return True
                # Reload
                elif event.unicode == 'r':
                    self.labyrinth = create_labyrinth(LAB_ROWS, LAB_COLS)
                    self.draw_labyrinth(None)
                    return True
                # Quit
                elif event.unicode == 'q':
                    pygame.quit()
                    exit(1)
        return False

    def run_algorithm(self):
        for state in (self.algorithm(self.labyrinth, Node(START, None))):
            if self.handle_event():
                return
            self.draw_labyrinth(state)
        self.algorithm = None

    def run(self):
        clear_window(self.screen)
        while True:
            self.handle_event()
            if self.labyrinth is not None and self.algorithm is not None:
                self.run_algorithm()




def create_labyrinth(rows: int, cols: int) -> Labyrinth:
    end = Location(rows - 2, cols - 2)
    return Labyrinth(rows, cols, .2, START, end)


def main():
    screen = create_window()

    Program(screen).run()

if __name__ == '__main__':
    main()