import math
import sys
from collections.abc import Generator
from typing import Callable

from data import Labyrinth, CellType, Location, Node
from data import SearchState, NodeStack, NodeQueue, NodePrioQueue


def search1(lab: Labyrinth, start: Node, state: SearchState, length_skip: Callable[[],int]) -> Generator[SearchState]:
    state.frontiers.push(start)
    state.frontier_locations = set[Location]()

    while not len(state.frontiers) == 0:
        curr_len = length_skip()
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
                    state.frontiers.push(Node(neighbor, current_node))
        yield state

    yield state
    return

def depth_first_search(lab: Labyrinth, start: Node) -> Generator[SearchState]:
    state = SearchState(NodeStack())
    return search1(lab, start, state, lambda: int(math.sqrt(len(state.frontiers))) + 1)

def breadth_first_search(lab: Labyrinth, start: Node) -> Generator[SearchState]:
    state = SearchState(NodeQueue())
    return search1(lab, start, state, lambda: len(state.frontiers))

def a_star_search(lab: Labyrinth, start: Node) -> Generator[SearchState]:
    state = SearchState(NodePrioQueue(lab.goal()))
    return search1(lab, start, state, lambda: int(math.sqrt(len(state.frontiers))) + 1)


def main():
    rows = 20 if len(sys.argv) < 2 else int(sys.argv[1])
    cols = 40 if len(sys.argv) < 3 else int(sys.argv[2])

    start = Location(0, 0)
    end = Location(rows - 2, cols - 2)
    lab = Labyrinth(rows, cols, .2, start, end)
    breadth_first_search(lab, Node(start, None))

if __name__ == '__main__':
    main()