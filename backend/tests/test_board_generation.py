import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app.game_logic import Minesweeper, EMPTY, MINE, COVERED, EMPTY_TILE, MINE_UNCOVERED, ERR

def test_board_init():
    width = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)
    assert len(game.hidden_board) == height
    assert len(game.hidden_board[0]) == width 

    for row in game.hidden_board:
        for cell in row:
            assert cell == EMPTY

    for row in game.visible_board:
            for cell in row:
                assert cell == COVERED

def test_place_mine_middle():
    width = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)
    game._place_mine(1,1)
    assert game.hidden_board ==  [[1,   1,    1], 
                            [1,   MINE, 1], 
                            [1, 1, 1]]

def test_place_mine_corner():
    width = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)
    game._place_mine(0,0)
    assert game.hidden_board ==  [[MINE,   1,    EMPTY], 
                            [1,     1 ,    EMPTY], 
                            [EMPTY, EMPTY, EMPTY]]

def test_place_2_mine():
    width = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)
    game._place_mine(0,0)
    game._place_mine(2,2)
    assert game.hidden_board ==  [[MINE,   1,    EMPTY], 
                            [1,     2 ,    1], 
                            [EMPTY, 1, MINE]]



def test_uncover_number():
    width = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)
    game.hidden_board = [[EMPTY,   1,    MINE], 
                        [EMPTY,   1,     1], 
                        [EMPTY, EMPTY, EMPTY]]

    game.uncover(0, 1)

    assert game.visible_board == [[COVERED,       1,    COVERED], 
                                 [COVERED,   COVERED,     COVERED], 
                                 [COVERED, COVERED, COVERED]]



def test_uncover_cascading_empty_board():
    width  = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)

    game.uncover(0, 0)

    assert game.visible_board == [[EMPTY_TILE, EMPTY_TILE, EMPTY_TILE],
                                 [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE],
                                 [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE]]

def test_uncover_cascading_empty_space():
    width = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)
    game.hidden_board = [[EMPTY,   1,    MINE], 
                  [EMPTY,   1,     1], 
                  [EMPTY, EMPTY, EMPTY]]

    game.uncover(0, 0)

    assert game.visible_board == [[EMPTY_TILE,   1,    COVERED], 
                                 [EMPTY_TILE,   1,     1], 
                                 [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE]]

def test_uncover_mine():
    width = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)
    game.hidden_board = [[EMPTY,   1,    MINE], 
                  [EMPTY,   1,     1], 
                  [EMPTY, EMPTY, EMPTY]]

    ret = game.uncover(0, 2)

    assert game.visible_board == [[COVERED,   COVERED,    MINE], 
                                  [COVERED,   COVERED,  COVERED], 
                                  [COVERED,   COVERED, COVERED]]
    assert ret == MINE_UNCOVERED
    assert game.status == MINE_UNCOVERED


def test_uncover_invalid_bounds():
    width = 3
    height = 3
    game = Minesweeper(width = width,
                        height = height,
                        num_mines = 0)
    game.hidden_board = [[EMPTY,   1,    MINE], 
                  [EMPTY,   1,     1], 
                  [EMPTY, EMPTY, EMPTY]]

    ret = game.uncover(0, 3)
    assert ret == ERR


