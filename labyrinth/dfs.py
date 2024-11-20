import sys
from collections.abc import Generator

from data import Labyrinth, CellType, Location, Node
from labyrinth.data import SearchState


def depth_first_search(lab: Labyrinth, start: Node) -> Generator[SearchState]:
    state = SearchState()

    state.frontiers.appendleft(start)
    state.frontier_locations = set[Location]()

    while not len(state.frontiers) == 0:
        curr_len = len(state.frontiers)
        for _ in range(curr_len):
            # get next node
            current_node = state.frontiers.pop()
            current_location = current_node.location
            state.frontier_locations.discard(current_location)
            state.visited_locations.add(current_location)
            # check current node for goal
            if lab.get_state(current_location).value == CellType.GOAL.value:
                state.result = current_node
                yield state
                return

            # get neighbors and push onto frontier
            neighbors = lab.get_neighbors(current_location)

            for neighbor in neighbors:
                if neighbor not in state.visited_locations and neighbor not in state.frontier_locations:
                    state.frontier_locations.add(neighbor)
                    state.frontiers.appendleft(Node(neighbor, current_node))
        yield state

    yield state
    return


def main():
    rows = 30 if len(sys.argv) < 2 else int(sys.argv[1])
    cols = 41 if len(sys.argv) < 3 else int(sys.argv[2])

    start = Location(0, 0)
    end = Location(rows - 2, cols - 2)
    lab = Labyrinth(rows, cols, .2, start, end)
    depth_first_search(lab, Node(start, None))

if __name__ == '__main__':
    main()