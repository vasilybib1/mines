"""
This file is responsible for board generation, game logic such as removal of tiles.
"""
import random

MINE = 'x'
EMPTY = 0
COVERED = '~'
EMPTY_TILE = ' '
FLAGGED = 'F'
MINE_UNCOVERED = 1
PERFECT = 0
ERR = -1
class Minesweeper:
    hidden_board = []
    visible_board = []
    width = -1
    height = -1
    status = PERFECT

    is_in_bounds = lambda self, x, y: self.width > x >= 0 and self.height > y >= 0

    def __init__(
        self,
        width,
        height,
        num_mines
    ):
        # init class attr.
        self.visible_board = [[COVERED for _ in range(width)] for _ in range(height)]
        self.hidden_board =  [[EMPTY for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        
        ## Assigning mines
        for _ in range(num_mines):
            mine_x = random.randrange(width)
            mine_y = random.randrange(height)
            # first we check if this place has a mine
            while (self.hidden_board[mine_x, mine_y] == MINE):
                mine_x = random.randrange(width)
                mine_y = random.randrange(height)

            self._place_mine(mine_x, mine_y)

    # places mine and updates board. separate function for testability.
    def _place_mine(self, mine_x, mine_y):
        self.hidden_board[mine_x][ mine_y] = MINE
        for x_delta in [-1, 0, 1]:
            for y_delta in [-1, 0, 1]:
                tile_x, tile_y = mine_x + x_delta, mine_y + y_delta
                if (self.is_in_bounds(tile_x, tile_y) and (self.hidden_board[tile_x][ tile_y] != MINE)): # edge guarding
                    self.hidden_board[tile_x][tile_y] += 1       
    
    def uncover(self, x, y):
        if not self.is_in_bounds(x,y):    
            return ERR

        if(self.hidden_board[x][y] == MINE):
            self.visible_board[x][y] = MINE
            self.handleMineDiscovered()
            return MINE_UNCOVERED

        else:
           self._check_for_cascade(x, y)

    def _check_for_cascade(self, x, y):

        if not self.is_in_bounds: return
        if self.visible_board[x][y] == COVERED: # means we need to uncover
            if self.hidden_board[x][y] == MINE: return 
            if self.hidden_board[x][y] == EMPTY:
                self.visible_board[x][y] = EMPTY_TILE
            else:
                self.visible_board[x][y] = self.hidden_board[x][y]
                return

            for x_delta in [-1, 0, 1]:
                for y_delta in [-1, 0, 1]:
                    tile_x, tile_y = x + x_delta, y + y_delta
                    if self.is_in_bounds(tile_x, tile_y): # edge guarding
                      self._check_for_cascade(tile_x, tile_y)   
            

    def handleMineDiscovered(self):
        self.status = MINE_UNCOVERED

    def toggle_flag(self, x,y):
        if self.visible_board[x][y] == FLAGGED:
            self.visible_board[x][y] = COVERED
        if self.visible_board == COVERED:
            self.visible_board[x][y] = FLAGGED


    def __str__(self):
        res = ""
        for row in self.hidden_board:
            for cell in row:
                res += str(cell) + " "
            res += "\n"

        return res

