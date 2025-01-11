import {AlgorithmNode, CellType, Labyrinth, SearchState, NodeStack, NodePrioQueue, PositionSet} from "./data"
import {Queue} from "@datastructures-js/queue";

export type SearchResult = Generator<SearchState, undefined, undefined>;

function* base_search(lab: Labyrinth, start: AlgorithmNode, state: SearchState, length_skip: () => number): SearchResult {
    state.frontiers.push(start);
    state.frontier_positions = new PositionSet();

    while(state.frontiers.size() != 0) {
        const current_length = length_skip()

        for (let i = 0; i < current_length; i++) {
            const current_node = state.frontiers.pop();
            const current_position = current_node.position;

            state.frontier_positions.delete(current_position);
            state.visited_positions.add(current_position);

            if(lab.get_state(current_position) == CellType.GOAL) {
                state.result = current_node;
                yield state;
                return;
            }

            const neighbours = lab.get_neighbours(current_position);

            for(const neighbourPosition of neighbours) {
                if(!state.visited_positions.has(neighbourPosition) && !state.frontier_positions.has(neighbourPosition)) {
                    state.frontier_positions.add(neighbourPosition);
                    state.frontiers.push(new AlgorithmNode(neighbourPosition, current_node))
                }
            }
        }
        yield state
    }

    yield state
    return;
}

export function depth_first_search(lab: Labyrinth, start: AlgorithmNode): SearchResult  {
    const state = new SearchState(new NodeStack())

    return base_search(lab, start, state, () => Math.floor(Math.sqrt(state.frontiers.size()))+1)
}

export function breadth_first_search(lab: Labyrinth, start: AlgorithmNode): SearchResult {
    const state = new SearchState(new Queue())

    return base_search(lab, start, state, () => state.frontiers.size());
}

export function a_star_search(lab: Labyrinth, start: AlgorithmNode): SearchResult {
    const state = new SearchState(new NodePrioQueue(lab.goal));
    return base_search(lab, start, state, () => Math.floor(Math.sqrt(state.frontiers.size()))+1);
}

export type AlgorithmFunction = (lab: Labyrinth, start: AlgorithmNode) => SearchResult
export type AlgorithmList = [AlgorithmFunction, string][]

export const ALGORITHM_LIST: AlgorithmList = [
    [breadth_first_search, "Breadth First Search"],
    [depth_first_search, "Depth First Search"],
    [a_star_search, "A* Search"],
]