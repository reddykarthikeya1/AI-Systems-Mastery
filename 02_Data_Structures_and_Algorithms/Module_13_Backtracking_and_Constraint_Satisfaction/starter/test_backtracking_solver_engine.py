"""Unit tests for BacktrackingSolverEngine."""
from backtracking_solver_engine import BacktrackingSolverEngine


def test_n_queens_4():
    solutions = BacktrackingSolverEngine.solve_n_queens(4)
    assert len(solutions) == 2
    for sol in solutions:
        assert len(sol) == 4
        # Verify 1 queen per row
        for row in sol:
            assert row.count("Q") == 1

def test_sudoku_solver():
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]
    ]
    solvable = BacktrackingSolverEngine.solve_sudoku(board)
    assert solvable
    # Ensure no empty cells remaining
    for row in board:
        assert "." not in row
        assert len(set(row)) == 9

def test_n_queens_1():
    solutions = BacktrackingSolverEngine.solve_n_queens(1)
    assert len(solutions) == 1
    assert solutions[0] == ["Q"]

def test_n_queens_2_and_3_impossible():
    assert len(BacktrackingSolverEngine.solve_n_queens(2)) == 0
    assert len(BacktrackingSolverEngine.solve_n_queens(3)) == 0
def test_sudoku_edge_cases():
    # Nearly complete board with 1 missing cell
    board = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "."]
    ]
    assert BacktrackingSolverEngine.solve_sudoku(board) is True
    assert board[8][8] == "9"
    
    # Contradictory board (1 missing cell with no valid candidate)
    unsolvable = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "."],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "2"]
    ]
    assert BacktrackingSolverEngine.solve_sudoku(unsolvable) is False


