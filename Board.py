from Tile import Tile

class Board:
    def __init__(self, pos, dim, rows, cols, mines, margin=0, rectangular=True):
        self.pos = pos.copy()
        self.dim = dim.copy()
        self.mines = mines
        self.flags = 0
        self.mines_placed = False
        w = self.dim.x / rows
        h = self.dim.y / cols
        if not rectangular:
            w = min(w, h)
            h = min(w, h)
        self.generateGrid(rows, cols, margin, w, h)
    
    def generateGrid(self, rows, cols, margin, w, h):
        self.grid = [[Tile(PVector(self.pos.x + r * w, self.pos.y + c * h), PVector(w-margin, h-margin, margin)) for c in range(cols)] for r in range(rows)]
    
    def placeMines(self, start=None):
        rows = len(self.grid)
        cols = len(self.grid[0])
        if rows * cols <= self.mines:
            for row in self.grid:
                for tile in row:
                    tile.is_bomb = True
        else:
            potential_mines = [PVector(i % cols, i // cols) for i in range(rows * cols)]
            if start is not None and start in potential_mines:
                if start.x > 0:
                    potential_mines.remove(PVector(start.x - 1, start.y))
                if start.y > 0:
                    potential_mines.remove(PVector(start.x, start.y - 1))
                if start.x < cols - 1:
                    potential_mines.remove(PVector(start.x + 1, start.y))
                if start.y < rows - 1:
                    potential_mines.remove(PVector(start.x, start.y + 1))
                if start.x > 0 and start.y > 0:
                    potential_mines.remove(PVector(start.x - 1, start.y - 1))
                if start.x < cols - 1 and start.y < rows - 1:
                    potential_mines.remove(PVector(start.x + 1, start.y + 1))
                if start.x > 0 and start.y < rows - 1:
                    potential_mines.remove(PVector(start.x - 1, start.y + 1))
                if start.x < cols - 1 and start.y > 0:
                    potential_mines.remove(PVector(start.x + 1, start.y - 1))
                potential_mines.remove(start)
            for _ in range(self.mines):
                position = potential_mines[int(random(len(potential_mines)))]
                potential_mines.remove(position)
                self.grid[int(position.y)][int(position.x)].is_bomb = True
        self.assignNumbers()
    
    def assignNumbers(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.grid[r][c].number = 0
                for xoff in range(-1, 2):
                    for yoff in range(-1, 2):
                        x = c + xoff
                        y = r + yoff
                        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]) and self.grid[y][x].is_bomb:
                            self.grid[r][c].number += 1

    def isWon(self):
        r = 0
        for row in self.grid:
            c = 0
            for tile in row:
                if not (tile.revealed or tile.is_bomb):
                    return False
                c += 1
            r += 1
        return True
    
    def show(self):
        for row in self.grid:
            for tile in row:
                tile.show()
    
    def floodFill(self, row, col):
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                c = col + xoff
                r = row + yoff
                if  0 <= r < len(self.grid) and 0 <= c < len(self.grid[r]):
                    if not (self.grid[r][c].is_bomb or self.grid[r][c].revealed):
                        empty, mine, wasflagged = self.grid[r][c].reveal()
                        if wasflagged is not None:
                            self.flags -= 1
                        if empty:
                            self.floodFill(r, c)
