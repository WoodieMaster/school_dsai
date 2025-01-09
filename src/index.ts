const canvas = document.getElementById('main') as HTMLCanvasElement;

const ctx = canvas.getContext('2d')!;

const COLOR_BG = "black"
const COLOR_OBSTACLE = "rgb(90,90,90)"
const COLOR_START = "pink"
const COLOR_GOAL = "cyan"
const COLOR_VISITED = "red"
const COLOR_FRONTIER = "yellow"
const COLOR_PATH = "green"




window.addEventListener("keydown", (e) => {

});

function startLoop(fn) {
    requestAnimationFrame(() => {
        if (fn()) {
            startLoop(fn)
        }
    });
}

function setSize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    clearWindow()
}

function clearWindow() {
    ctx.fillStyle = COLOR_BG
    ctx.fillRect(0, 0, canvas.width, canvas.height)
}

function setTitle(title: string) {
    document.title = title
}

function drawLabyrinth(labyrinth, search_state) {
    clearWindow()
    const cell_height = canvas.height / labyrinth.rows()
    const cell_width = canvas.width / labyrinth.cols()
    const inset = .1

    const result_path = new Set()

    if (search_state != null && search_state.result != null) {
        let node = search_state.result
        while (node.parent != null) {
            result_path.add(node.location)
            node = node.parent
        }
    }

    for (let row_idx = 0; row_idx < labyrinth.grid_items(); row_idx++) {
        const cols = labyrinth.grid_items()[row_idx]

        for (let col_idx = 0; col_idx < labyrinth.cols(); col_idx++) {
            const cell = cols[col_idx]

            const start_pos_x = col_idx * cell_width + cell_width * inset
            const start_pos_y = row_idx * cell_height + cell_height * inset

            const draw_width = cell_width * (1 - (inset * 2))
            const draw_height = cell_height * (1 - (inset * 2))

            let color = null
            if (cell.type === cellTypes.OBSTACLE) {
                color = COLOR_OBSTACLE
            } else if (cell.type === cellTypes.START) {
                color = COLOR_START
            } else if (cell.type === cellTypes.GOAL) {
                color = COLOR_GOAL
            } else if (search_state != null) {
                const pos = new Position(row_idx, col_idx)

                if(result_path.has(pos)) {
                    color = COLOR_PATH
                }else if (search_state.visited_locations.has(pos)) {
                    color = COLOR_VISITED
                }else if (search_state.frontier_locations.has(pos)) {
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

window.onresize = setSize

setSize();