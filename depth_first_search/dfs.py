import random
import time
import os

width = 20
height = 10

def main():
    grid = [[' ' for _x in range(width)] for _y in range(height)]

    start_pos = (random.randint(0,width-1), random.randint(0,height-1))
    end_pos = (random.randint(0,width-1), random.randint(0,height-1))

    grid[start_pos[1]][start_pos[0]] = 'S'
    grid[end_pos[1]][end_pos[0]] = 'G'

    solve(grid, start_pos)


def print_grid(grid: list[list[str]]):
    os.system("cls")
    print('+' + '-' * width + '+')
    for row in grid:
        print('|' + "".join(row) + '|')
    print('+' + '-' * width + '+')

def add_to_stack(grid: list[list[str]], stack: list[tuple[int,int]], pos: tuple[int, int]):
    if pos not in stack:
        stack.append(pos)
    if grid[pos[1]][pos[0]] == ' ':
        grid[pos[1]][pos[0]] = ':'
def solve(grid: list[list[str]],pos: tuple[int,int]):
    stack: list[tuple[int,int]] = [pos]

    while True:
        curr_pos = stack.pop()

        curr_ch = grid[curr_pos[1]][curr_pos[0]]
        if curr_ch == 'G':
            return

        grid[curr_pos[1]][curr_pos[0]] = '@'

        if curr_pos[1] > 0:
            add_to_stack(grid, stack, (curr_pos[0],curr_pos[1]-1))

        if curr_pos[1] < height - 1:
            add_to_stack(grid, stack, (curr_pos[0],curr_pos[1]+1))


        if curr_pos[0] > 0:
            add_to_stack(grid, stack, (curr_pos[0]-1,curr_pos[1]))


        if curr_pos[0] < width - 1:
            add_to_stack(grid, stack, (curr_pos[0]+1,curr_pos[1]))

        print_grid(grid)

        if curr_ch == ':':
            grid[curr_pos[1]][curr_pos[0]] = '#'

        time.sleep(.1)


if __name__ == '__main__':
    main()

