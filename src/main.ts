import {AlgorithmNode, CellType, enumerate, Labyrinth, NodePrioQueue, Position, PositionSet, SearchState} from "./data";
import {ALGORITHM_LIST, AlgorithmFunction, SearchResult} from "./algorithms";
import {PriorityQueue} from "@datastructures-js/priority-queue";

const canvas = document.getElementById('main') as HTMLCanvasElement;

const ctx = canvas.getContext('2d')!;

const COLOR_BG = "black"
const COLOR_OBSTACLE = "rgb(90,90,90)"
const COLOR_START = "pink"
const COLOR_GOAL = "cyan"
const COLOR_VISITED = "red"
const COLOR_FRONTIER = "yellow"
const COLOR_PATH = "green"


const LAB_ROWS = 100;
const LAB_COLS = 100;
const START_POS = new Position(Math.floor(LAB_ROWS / 2), Math.floor(LAB_COLS / 2));
const END_POS = new Position(LAB_ROWS - 2, LAB_COLS - 2);
const OBSTACLE_DENSITY = .2

function setSize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    drawLabyrinth(currentState);
}

function resetWindow() {
    ctx.fillStyle = COLOR_BG;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function setTitle(title: string) {
    document.title = title
}

let selectedAlgorithm: AlgorithmFunction | undefined;
let labyrinth: Labyrinth | undefined;
let simulated: boolean = false;
let runningAlgorithm: SearchResult | undefined;
let currentState: SearchState | undefined;
let active = true;

function drawLabyrinth(search_state: SearchState | undefined) {
    resetWindow();
    if(labyrinth === undefined) return;

    const cell_height = canvas.height / labyrinth.rows
    const cell_width = canvas.width / labyrinth.cols
    const inset = .1

    const result_path = new PositionSet();

    if (search_state != null && search_state.result != null) {
        let node = search_state.result
        while (node.parent != null) {
            result_path.add(node.position)
            node = node.parent
        }
    }

    for (const [row_idx, cols] of enumerate(labyrinth.grid)) {
        for (const [col_idx, cell] of enumerate(cols)) {
            const start_pos_x = col_idx * cell_width + cell_width * inset
            const start_pos_y = row_idx * cell_height + cell_height * inset

            const draw_width = cell_width * (1 - (inset * 2))
            const draw_height = cell_height * (1 - (inset * 2))

            let color = null
            if (cell === CellType.OBSTACLE) {
                color = COLOR_OBSTACLE
            } else if (cell === CellType.START) {
                color = COLOR_START
            } else if (cell === CellType.GOAL) {
                color = COLOR_GOAL
            } else if (search_state != null) {
                const pos = new Position(row_idx, col_idx)

                if(result_path.has(pos)) {
                    color = COLOR_PATH
                }else if (search_state.visited_positions.has(pos)) {
                    color = COLOR_VISITED
                }else if (search_state.frontier_positions.has(pos)) {
                    color = COLOR_FRONTIER
                }
            }

            if (color !== null) {
                ctx.fillStyle = color
                ctx.fillRect(start_pos_x, start_pos_y, draw_width, draw_height)
            }
        }
    }

}

function select_algorithm(algorithm_idx: number) {
    if(labyrinth === undefined) {
        labyrinth = create_labyrinth();
    }
    if (algorithm_idx >= ALGORITHM_LIST.length) {
        alert(`Invalid algorithm idx ${algorithm_idx}! Max index: ${ALGORITHM_LIST.length - 1}`);
        return
    }

    const [newAlgorithm, name] = ALGORITHM_LIST[algorithm_idx];
    selectedAlgorithm = newAlgorithm;

    setTitle("Search Algorithm - " + name);


    start_algorithm();
}

function handle_event(e: KeyboardEvent) {
    if(e.key.length != 1) {
        return;
    }
    const code = e.key.charCodeAt(0);
    if(code >= '0'.charCodeAt(0) && code <= '9'.charCodeAt(0)) {
        select_algorithm(code - '1'.charCodeAt(0))
        return
    }

    if(e.key == 'r') {
        labyrinth = create_labyrinth();
        if(runningAlgorithm) {
            runningAlgorithm = selectedAlgorithm?.(labyrinth, new AlgorithmNode(START_POS));
        }
        drawLabyrinth(undefined);
        return
    }

    if (e.key == 'p') {
        if(active) {
            active = false;
        }else {
            active = true;
            run_algorithm_step();
        }
        return;
    }

    if(e.key == 'f') {
        simulated = !simulated;
    }
}

function start_algorithm() {
    simulated = true;
    active = true;
    if(selectedAlgorithm === undefined) {
        selectedAlgorithm = ALGORITHM_LIST[0][0];
    }
    if(labyrinth === undefined) {
        labyrinth = create_labyrinth();
    }

    runningAlgorithm = selectedAlgorithm(labyrinth, new AlgorithmNode(START_POS));

    run_algorithm_step()

}

function stop_algorithm() {
    runningAlgorithm = undefined;
}

function run_algorithm_step() {
    if(runningAlgorithm === undefined || !active) return;

    currentState = runningAlgorithm.next().value;

    if(currentState === undefined) {
        return stop_algorithm();
    }

    if(simulated || currentState.result !== undefined) {
        drawLabyrinth(currentState);
    }

    requestAnimationFrame(run_algorithm_step);
}

function testPrioQueue() {
    const queue = new NodePrioQueue(new Position(0,0));

    for(let i = 0; i < 10; i++) {
        queue.push(new AlgorithmNode(new Position(0, Math.floor(Math.random() * 100))));
    }

    queue.pop();
    queue.pop();
    queue.pop();

    for(let i = 0; i < 10; i++) {
        queue.push(new AlgorithmNode(new Position(0, Math.floor(Math.random() * 100))));
    }

    for(const el of queue.data) {
        console.log(el[0].position, el[1]);
    }
}

function create_labyrinth(): Labyrinth {
    return new Labyrinth(LAB_ROWS, LAB_COLS, OBSTACLE_DENSITY, START_POS, END_POS);
}

window.addEventListener("keydown", handle_event);
window.onresize = setSize

labyrinth = create_labyrinth();
setSize();

testPrioQueue();
