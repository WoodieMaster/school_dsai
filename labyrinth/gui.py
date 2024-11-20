import time

import pygame
from pygame import Surface

import dfs
from labyrinth.data import Location, Labyrinth, Node

pygame.init()

LAB_ROWS = 150
LAB_COLS = 200
SCALE = 5
START = Location(0,0)

background_colour = (0,0,0)

def create_window() -> Surface:
    screen = pygame.display.set_mode((LAB_COLS * SCALE, LAB_ROWS * SCALE))

    pygame.display.set_caption('Search Algorithms')

    clear_window(screen)

    return screen

def clear_window(screen: Surface):
    screen.fill(background_colour)

def game_loop(screen: Surface, lab: Labyrinth | None):
    clear_window(screen)

    while True:
        if lab is not None:
            for state in dfs.depth_first_search(lab, Node(START, None)):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                clear_window(screen)
                lab.draw(screen, state)
                # time.sleep(0)
            lab = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'r':
                    lab = create_labyrinth(LAB_ROWS, LAB_COLS)


def create_labyrinth(rows: int, cols: int) -> Labyrinth:
    end = Location(rows - 2, cols - 2)
    return Labyrinth(rows, cols, .2, START, end)


def main():

    screen = create_window()

    game_loop(screen, create_labyrinth(LAB_ROWS, LAB_COLS))

if __name__ == '__main__':
    main()