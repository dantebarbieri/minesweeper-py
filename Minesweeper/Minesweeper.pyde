from Board import Board
from Bot import Bot
import random as rand

bg = [0, 0, 0, 0.0025]
board = None
board_coords = [PVector(), PVector()]
board_dims = PVector()
gameover = None
win_color = color(124, 201, 124)
lose_color = color(201, 124, 124)
resolution_desc = ''
robbie = None

def setup():
    global bg, board, board_coords, board_dims, gameover, resolution_desc, robbie
    # size(1280, 720)
    # size(rand.randint(480, 3840), rand.randint(480, 2160))
    fullScreen()
    rows = 30
    cols = 16
    resolution_desc = 'Size: ' + str(rows) + ' x ' + str(cols)
    mines = 60
    board_start = PVector(width / 20, height / 8)
    board_size = PVector(width / 1.3333333, height / 1.3333333)
    board_coords[0] = board_start
    board_coords[1] = PVector.add(board_start, board_size)
    board_dims = board_size.copy()
    board = Board(board_start, board_size, rows, cols, mines, margin=board_dims.x/280, rectangular=rows==cols)
    gameover = False
    robbie = Bot(board)
    bg[0] = random(10000)
    bg[1] = random(10000)
    bg[2] = random(10000)

def draw():
    global bg, gameover
    background(255*noise(bg[0]), 255*noise(bg[1]), 255*noise(bg[2]))
    time = str(round(millis() / float(1000), 2))
    textSize(width / 75)
    textAlign(LEFT)
    fill(51)
    if gameover:
        noLoop()
        background(lose_color)
        text('Game Over\nTime: ' + time, board_coords[1].x + board_dims.x / 100, board_coords[0].y + board_dims.y / 100)
    elif gameover is None:
        noLoop()
        background(win_color)
        text('You Win!\nTime: ' + time, board_coords[1].x + board_dims.x / 100, board_coords[0].y + board_dims.y / 50)
    else:
        text('Time Elapsed: ' + time, board_coords[1].x + board_dims.x / 100, board_coords[0].y + board_dims.y / 100)
    text('Flags: ' + str(board.flags) + '/' + str(board.mines), board_coords[1].x + board_dims.x / 100, board_coords[0].y + height / 15)
    text(resolution_desc, board_coords[1].x + board_dims.x / 75, board_coords[0].y + board_dims.y / 5)
    board.show()
    for v in bg[:-1]:
        v += bg[-1]
    result = robbie.play()
    if robbie.gameover:
        gameover = True
    elif robbie.gameover is None:
        gameover = None

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
                    board.flag(r, c)
                    return None
                    
