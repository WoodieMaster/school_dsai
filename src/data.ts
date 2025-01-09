import {Queue} from "@datastructures-js/queue"

enum CellType {
    EMPTY = ' ',
    OBSTACLE = '#',
    START = 'S',
    GOAL = 'G',
}

class Position {
    row: number;
    column: number;

    constructor(row: number, column: number) {
        this.row = row;
        this.column = column;
    }
}

class AlgorithmNode {
    position: Position;
    parent?: AlgorithmNode;

    constructor(position: Position, parent?: AlgorithmNode) {
        this.position = position;
        this.parent = parent;
    }
}

interface Frontier {
    push(value: Node): void;
    pop(): Node;
    size(): number;
}

class Stack implements Frontier{
    data: Node[] = [];

    push(value: Node) {
        this.data.push(value);
    }

    pop(): Node {
        return this.data.pop()!;
    }

    size(): number {
        return this.data.length;
    }
}

class SearchState {
    frontiers: Frontier;
    visited_positions = new Set<Position>();
    result?: AlgorithmNode;
    frontier_positions = new Set<Position>();

    constructor(frontiers: Frontier) {
        this.frontiers = frontiers
    }
}

class Labyrinth {
    rows: number;
    cols: number;
    obstacle_density: number;
    start: Position;
    goal: Position;
    grid: CellType[][];


    constructor(rows: number, cols: number, obstacle_density: number, start: Position, goal: Position) {
        this.rows = rows;
        this.cols = cols;
        this.obstacle_density = obstacle_density;
        this.start = start;
        this.goal = goal;
        this.grid = Array.from({length: rows}, () => Array.from({length: cols}, () => CellType.EMPTY));
    }

    private check_location(row: number, col: number) {
        return 0 <= row && row < this.rows && 0 <= col && col < this.cols && this.grid[row][col] != CellType.OBSTACLE
    }

    get_neighbours(pos: Position): Position[] {
        const neighbors: Position[] = [];

        if (this.check_location(pos.row, pos.column - 1))
            neighbors.push(new Position(pos.row, pos.column - 1))

        if (this.check_location(pos.row, pos.column + 1))
            neighbors.push(new Position(pos.row, pos.column + 1))

        if (this.check_location(pos.row - 1, pos.column))
            neighbors.push(new Position(pos.row - 1, pos.column))

        if (this.check_location(pos.row + 1, pos.column))
            neighbors.push(new Position(pos.row + 1, pos.column))
        return neighbors
    }

    get_state(pos: Position): CellType  {
        return this.grid[pos.row][pos.column];
    }

    private fill_with_obstacles() {
        for (const cols of this.grid) {
            for (let i = 0; i < cols.length; i++) {
                if (Math.random() < this.obstacle_density) {
                    cols[i] = CellType.OBSTACLE;
                }
            }
        }

        this.grid[this.start.row][this.start.column] = CellType.START;
        this.grid[this.goal.row][this.goal.column] = CellType.GOAL;
    }
}