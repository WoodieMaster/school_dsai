from data import Labyrinth, CellType, Location, Stack, Node


def main():
    rows = 5
    cols = 13

    lab = Labyrinth(rows, cols, .5, Location(0,0), Location(1,1))

    print(str(lab), str(lab).count(str(CellType.OBSTACLE.value)), rows * cols)

    stack: Stack[Node]= Stack()
    stack.push(Node(0))
    print(stack)

    print(lab.get_neighbors(Location(rows-1,cols-1)))

if __name__ == '__main__':
    main()