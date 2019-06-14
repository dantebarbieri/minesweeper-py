from Board import Board

bg = [0, 0, 0, 0.0025]
board = None
gameover = None
win_color = color(124, 201, 124)
lose_color = color(201, 124, 124)
resolution_desc = ''

def setup():
    global bg, board, gameover, resolution_desc
    # size(1920, 1080)
    fullScreen()
    rows = 30
    cols = 16
    resolution_desc = 'Size: ' + str(rows) + ' x ' + str(cols)
    mines = 99
    board = Board(PVector(width / 20, height / 8), PVector(width / 1.3333333, height / 1.3333333), rows, cols, mines, margin=12, rectangular=rows==cols)
    gameover = False
    bg[0] = random(10000)
    bg[1] = random(10000)
    bg[2] = random(10000)

def draw():
    global bg
    background(255*noise(bg[0]), 255*noise(bg[1]), 255*noise(bg[2]))
    time = str(round(millis() / float(1000), 2))
    textSize(36)
    textAlign(LEFT)
    fill(51)
    if gameover:
        noLoop()
        background(lose_color)
        text('Game Over\nTime: ' + time, width / 1.25, height / 4)
    elif gameover is None:
        noLoop()
        background(win_color)
        text('You Win!\nTime: ' + time, width / 1.25, height / 4)
    else:
        text('Time Elapsed: ' + time, width / 1.25, height / 4)
    text('Flags: ' + str(board.flags) + '/' + str(board.mines), width / 1.25, height / 3)
    text(resolution_desc, width / 1.2, height / 2)
    board.show()
    for v in bg[:-1]:
        v += bg[-1]

def mousePressed():
    global gameover
    if mouseButton == LEFT:
        for r in range(len(board.grid)):
            for c in range(len(board.grid[r])):
                if board.grid[r][c].isHovered():
                    if not board.mines_placed:
                        board.placeMines(PVector(c, r))
                        board.mines_placed = True
                    if not board.grid[r][c].revealed and board.grid[r][c].flagged is None:
                        empty, bomb, wasflagged = board.grid[r][c].reveal()
                        if empty:
                            board.floodFill(r, c)
                        elif bomb:
                            gameover = True
                        if wasflagged is not None:
                            board.flags -= 1
                        if board.isWon():
                            gameover = None
                    elif board.grid[r][c].revealed and board.grid[r][c].flag_count >= board.grid[r][c].number:
                        for xoff in range(-1, 2):
                            for yoff in range(-1, 2):
                                y = r + yoff
                                x = c + xoff
                                if 0 <= y < len(board.grid) and 0 <= x < len(board.grid[y]) and board.grid[y][x].flagged is None:
                                    empty, bomb, wasflagged = board.grid[y][x].reveal()
                                    if empty:
                                        board.floodFill(y, x)
                                    elif bomb:
                                        gameover = True
                                    if wasflagged is not None:
                                        board.flags -= 1
                                    if board.isWon():
                                        gameover = None
                    return None
    elif mouseButton == RIGHT:
        for r in range(len(board.grid)):
            for c in range(len(board.grid[r])):
                if board.grid[r][c].isHovered():
                    if board.grid[r][c].flagged is None:
                        board.grid[r][c].flagged = True
                        delta = 1
                    elif board.grid[r][c].flagged:
                        board.grid[r][c].flagged = False
                        delta = 0
                    else:
                        board.grid[r][c].flagged = None
                        delta = -1
                    board.flags += delta
                    for xoff in range(-1, 2):
                        for yoff in range(-1, 2):
                            y = r + yoff
                            x = c + xoff
                            if 0 <= y < len(board.grid) and 0 <= x < len(board.grid[y]):
                                board.grid[y][x].flag_count += delta
                    return None
                    
