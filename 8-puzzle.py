import numpy as np
from queue import PriorityQueue, Queue
from collections import deque

class PuzzleState:
    def __init__(self, board, blank_row, blank_col, parent=None, move=None, depth=0, cost=0):
        self.board = np.array(board)
        self.blank_row = blank_row
        self.blank_col = blank_col
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    # Check if this state is the goal state
    def is_goal(self):
        goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        return np.array_equal(self.board, goal)

    # Generate the hash code for the current board configuration
    def __hash__(self):
        return hash(self.board.tobytes())

    # Check if two PuzzleStates are equal
    def __eq__(self, other):
        return np.array_equal(self.board, other.board)
    
    # For priority queue to compare PuzzleState objects
    def __lt__(self, other):
        return self.cost < other.cost

def move_blank(state, move, move_name):
    new_row = state.blank_row + move[0]
    new_col = state.blank_col + move[1]

    if 0 <= new_row < 3 and 0 <= new_col < 3:
        new_board = state.board.copy()
        new_board[state.blank_row, state.blank_col], new_board[new_row, new_col] = new_board[new_row, new_col], new_board[state.blank_row, state.blank_col]

        return PuzzleState(new_board, new_row, new_col, state, move_name, state.depth + 1, 0)

    return None

def calculate_heuristic(state):
    heuristic = 0
    for r in range(3):
        for c in range(3):
            tile = state.board[r, c]
            if tile != 0:
                goal_row = (tile - 1) // 3
                goal_col = (tile - 1) % 3
                heuristic += abs(goal_row - r) + abs(goal_col - c)
    return heuristic

def print_solution(state):
    path = deque()
    while state:
        path.appendleft(state)
        state = state.parent
    for s in path:
        print(s.move)
        print_board(s.board)
    print("--------------------------")

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))
    print()

def dfs(start_state):
    visited = set()
    stack = [start_state]

    while stack:
        current = stack.pop()
        if current.is_goal():
            print_solution(current)
            return

        visited.add(current)

        for move, move_name in [((0, 1), "Right"), ((1, 0), "Down"), ((0, -1), "Left"), ((-1, 0), "Up")]:
            next_state = move_blank(current, move, move_name)
            if next_state and next_state not in visited:
                stack.append(next_state)

    print("No solution found")

def bfs(start_state):
    visited = set()
    queue = deque([start_state])

    while queue:
        current = queue.popleft()
        if current.is_goal():
            print_solution(current)
            return

        visited.add(current)

        for move, move_name in [((0, 1), "Right"), ((1, 0), "Down"), ((0, -1), "Left"), ((-1, 0), "Up")]:
            next_state = move_blank(current, move, move_name)
            if next_state and next_state not in visited:
                queue.append(next_state)

    print("No solution found")

def a_star(start_state):
    open_list = PriorityQueue()
    closed_list = set()

    start_state.cost = calculate_heuristic(start_state)
    open_list.put((start_state.cost, start_state))

    while not open_list.empty():
        current = open_list.get()[1]

        if current.is_goal():
            print_solution(current)
            return

        closed_list.add(current)

        for move, move_name in [((0, 1), "Right"), ((1, 0), "Down"), ((0, -1), "Left"), ((-1, 0), "Up")]:
            next_state = move_blank(current, move, move_name)
            if next_state and next_state not in closed_list:
                next_state.cost = next_state.depth + calculate_heuristic(next_state)
                open_list.put((next_state.cost, next_state))

    print("No solution found")

def main():
    print("---------------------------------------------")
    print("\t *** 8-Puzzle Problem ***")
    print("---------------------------------------------")

    initial_board = [[1, 0, 3], [4, 2, 5], [7, 8, 6]]
    goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    print("Initial state:")
    print_board(initial_board)

    print("Goal state:")
    print_board(goal_board)
    print("---------------------------------------------")

    start_state = PuzzleState(initial_board, 0, 1)

    print("BFS Solution:")
    bfs(start_state)

    print("A* Solution:")
    a_star(start_state)

if __name__ == "__main__":
    main()
