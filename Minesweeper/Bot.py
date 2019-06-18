class Bot:
    def __init__(self, b):
        self.gameover = False
        self.board = b
    
    def play(self):
        if not self.board.mines_placed:
            self.firstMove()
        else:
            for i in range(len(self.board.grid)):
                for j in range(len(self.board.grid[i])):
                    if self.flagAll(i, j):
                        return None
                    self.revealAll(i, j)
    
    def firstMove(self):
        row = int(random(len(self.board.grid)))
        col = int(random(len(self.board.grid[row])))
        self.board.placeMines(PVector(col, row))
        self.board.mines_placed = True
        empty, bomb, wasflagged = self.board.grid[row][col].reveal()
        if empty:
            self.board.floodFill(row, col)
        elif bomb:
            self.gameover = True
        elif self.board.isWon():
            self.gameover = None
        if wasflagged is not None:
            self.board.flags -= 1
    
    def flagAll(self, row, col):
        hidden = self.countNotRevealed(row, col)
        flagged = False
        if hidden > 0 and self.board.grid[row][col].revealed and hidden == self.board.grid[row][col].number:
            for xoff in range(-1, 2):
                for yoff in range(-1, 2):
                    x = col + xoff
                    y = row + yoff
                    if 0 <= y < len(self.board.grid) and 0 <= x < len(self.board.grid[y]):
                        if not self.board.grid[y][x].revealed and self.board.grid[y][x].flagged is None:
                            flagged = True
                            self.board.flag(y, x)
        return flagged
        
    def revealAll(self, row, col):
        revealed = False
        if self.board.grid[row][col].revealed and self.board.grid[row][col].flag_count == self.board.grid[row][col].number:
            for xoff in range(-1, 2):
                for yoff in range(-1, 2):
                    x = col + xoff
                    y = row + yoff
                    if 0 <= y < len(self.board.grid) and 0 <= x < len(self.board.grid[y]):
                        if not self.board.grid[y][x].revealed and self.board.grid[y][x].flagged is None:
                            revealed = True
                            empty, bomb, wasflagged = self.board.grid[y][x].reveal()
                            if empty:
                                self.board.floodFill(y, x)
                            elif bomb:
                                self.gameover = True
                            elif self.board.isWon():
                                self.gameover = None
                            if wasflagged is not None:
                                self.board.flags -= 1
        return revealed
    
    def countNotRevealed(self, row, col):
        count = 0
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                x = col + xoff
                y = row + yoff
                if 0 <= y < len(self.board.grid) and 0 <= x < len(self.board.grid[y]):
                     if x != col or y != row:
                         if not self.board.grid[y][x].revealed:
                             count += 1
        return count

    def countHidden(self, row, col):
        count = 0
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                x = col + xoff
                y = row + yoff
                if 0 <= y < len(self.board.grid) and 0 <= x < len(self.board.grid[y]):
                     if x != col or y != row:
                         if not self.board.grid[y][x].revealed and self.board.grid[y][x].flagged is None:
                             count += 1
        return count
    
    def countRevealed(self, row, col, force_revealed=True):
        if 0 <= row < len(self.board.grid) and 0 <= col < len(self.board.grid[row]):
            if force_revealed and not self.board.grid[row][col].revealed:
                return None
            count = 0
            for xoff in range(-1, 2):
                for yoff in range(-1, 2):
                    x = col + xoff
                    y = row + yoff
                    if 0 <= y < len(self.board.grid) and 0 <= x < len(self.board.grid[y]):
                        if self.board.grid[y][x].revealed:
                            count += 1
            return count
        else:
            raise Exception("The piece whose neighbors you attempted to count revealed is not in the board!")
    
    def countPlayable(self, row, col, force_hidden=True):
        if 0 <= row < len(self.board.grid) and 0 <= col < len(self.board.grid[row]):
            revealed = self.countRevealed(row, col, not force_hidden)
            if revealed is None:
                return None
            else:
                return 9 - (revealed + self.board.grid[row][col].flag_count)
    
