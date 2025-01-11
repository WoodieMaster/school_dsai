import {PriorityQueue} from "@datastructures-js/priority-queue";

interface Enumerable<T> extends Iterable<T>{
    readonly length: number;

    [index: number]: T;
}

export function* enumerate<T>(data: Enumerable<T>): Generator<[number, T]> {
    for(let i = 0; i < data.length; i++) yield [i, data[i]];
}

export enum CellType {
    EMPTY = ' ',
    OBSTACLE = '#',
    START = 'S',
    GOAL = 'G',
}

export class Position {
    row: number;
    column: number;

    constructor(row: number, column: number) {
        this.row = row;
        this.column = column;
    }
}

export class AlgorithmNode {
    position: Position;
    parent?: AlgorithmNode;

    constructor(position: Position, parent?: AlgorithmNode) {
        this.position = position;
        this.parent = parent;
    }
}

export interface Frontier {
    push(value: AlgorithmNode): void;
    pop(): AlgorithmNode;
    size(): number;
}

export class NodeStack implements Frontier {
    data: AlgorithmNode[] = [];

    push(value: AlgorithmNode) {
        this.data.push(value);
    }

    pop(): AlgorithmNode {
        return this.data.pop()!;
    }

    size(): number {
        return this.data.length;
    }
}

export type NodePrioQueueEntry = [AlgorithmNode, number];

export class NodePrioQueue implements Frontier {
    data = new PriorityQueue<NodePrioQueueEntry>(
        (a,b)=>
            this.calculate_cost(a) - this.calculate_cost(b)
    );
    step_count = 0;
    target: Position

    constructor(target: Position) {
        this.target = target;
    }

    private calculate_cost(entry: NodePrioQueueEntry): number {
        return Math.abs(entry[0].position.row - this.target.row) + Math.abs(entry[0].position.column - this.target.column) + entry[1]
    }

    push(value: AlgorithmNode) {
        this.data.enqueue([value, this.step_count+1]);
    }

    pop(): AlgorithmNode {
        const [node, step_count] = this.data.dequeue()!;
        this.step_count = step_count;
        return node;
    }

    size(): number {
        return this.data.size();
    }
}

export class SearchState {
    frontiers: Frontier;
    visited_positions = new PositionSet();
    result?: AlgorithmNode;
    frontier_positions = new PositionSet();

    constructor(frontiers: Frontier) {
        this.frontiers = frontiers
    }
}

export class Labyrinth {
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
        this.grid = Array.from(
            {length: rows},
            () => Array.from(
                {length: cols},
                () => CellType.EMPTY
            )
        );

        this.fill_with_obstacles();
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

export class PositionSet {
    data = new Set<string>();

    add(pos: Position) {
        this.data.add(this.toItem(pos));
    }

    delete(pos: Position) {
        this.data.delete(this.toItem(pos))
    }

    private toItem(pos: Position): string {
        return pos.row.toString() + "," + pos.column.toString();
    }

    has(pos: Position) {
        return this.data.has(this.toItem(pos));
    }
}