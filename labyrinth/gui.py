import time
from collections.abc import Callable, Generator

import pygame
from pygame import Surface

import algorithms
from labyrinth.data import Location, Labyrinth, Node, clear_window

pygame.init()

LAB_ROWS = 190
LAB_COLS = 300
SCALE = 3
START = Location(LAB_ROWS // 2, LAB_COLS // 2)


search_algorithms: list[tuple[Callable[[Labyrinth, Node], Generator[algorithms.SearchState, None, None]],str]] = [
    (algorithms.breadth_first_search, "Breadth First Search"),
    (algorithms.depth_first_search, "Depth First Search")
]

def create_window() -> Surface:
    screen = pygame.display.set_mode((LAB_COLS * SCALE, LAB_ROWS * SCALE))

    pygame.display.set_caption('Search Algorithms')

    clear_window(screen)

    return screen

def game_loop(screen: Surface):
    clear_window(screen)

    algorithm = None

    lab = create_labyrinth(LAB_ROWS, LAB_COLS)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if len(event.unicode) != 1:
                    continue
                if ord(event.unicode) in range(ord('0'),ord('9')+1):
                    lab = create_labyrinth(LAB_ROWS, LAB_COLS)
                    info = search_algorithms[int(event.unicode)]
                    algorithm = info[0]
                    pygame.display.set_caption('Search Algorithms - ' + info[1])
                elif event.unicode == 'r':
                    lab = create_labyrinth(LAB_ROWS, LAB_COLS)
                    lab.draw(screen, None)
        if lab is not None and algorithm is not None:
            for state in (algorithm(lab, Node(START, None))):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                lab.draw(screen, state)
                # time.sleep(0)
            algorithm = None



def create_labyrinth(rows: int, cols: int) -> Labyrinth:
    end = Location(rows - 2, cols - 2)
    return Labyrinth(rows, cols, .2, START, end)


def main():
    screen = create_window()

    game_loop(screen)

if __name__ == '__main__':
    main()