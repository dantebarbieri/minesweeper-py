from Board import Board
from Bot import Bot
import random as rand

bg = [0, 0, 0, 0.0025]
board = None
board_coords = [PVector(), PVector()]
board_dims = PVector()
gameover = None
initial_time = None
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
    mines = 99
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

def getTimeDiff(initial):
    if initial is None:
        return "STOPPED"
    ss = (millis() - initial) / float(1000)
    mm = int(ss // 60)
    if mm > 0:
        ss = (millis() - initial) % 60000 / float(1000)
    hh = mm // 60
    if hh > 0:
        mm %= 60
    dd = hh // 24
    if dd > 0:
        hh %= 24
    ww = dd // 7
    if ww > 0:
        dd %= 7
    secondPrefix = "0"*(2-len(str(int(ss))))
    result = secondPrefix + str(round(ss, 2))
    if mm > 0 or hh > 0 or dd > 0 or ww > 0:
        result = str(mm).zfill(2) + ":" + result
    if hh > 0 or dd > 0 or ww > 0:
        result = str(hh).zfill(2) + ":" + result
    if dd > 0 or ww > 0:
        result = str(dd).zfill(2) + ":" + result
    if ww > 0:
        result = str(ww).zfill(2) + ":" + result
    return result

def getTime():
    ss = millis() / float(1000)
    mm = int(ss // 60)
    if mm > 0:
        ss = millis() % 60000 / float(1000)
    hh = mm // 60
    if hh > 0:
        mm %= 60
    dd = hh // 24
    if dd > 0:
        hh %= 24
    ww = dd // 7
    if ww > 0:
        dd %= 7
    secondPrefix = "0"*(2-len(str(int(ss))))
    result = secondPrefix + str(round(ss, 2))
    if mm > 0 or hh > 0 or dd > 0 or ww > 0:
        result = str(mm).zfill(2) + ":" + result
    if hh > 0 or dd > 0 or ww > 0:
        result = str(hh).zfill(2) + ":" + result
    if dd > 0 or ww > 0:
        result = str(dd).zfill(2) + ":" + result
    if ww > 0:
        result = str(ww).zfill(2) + ":" + result
    return result

def draw():
    global bg, gameover
    background(255*noise(bg[0]), 255*noise(bg[1]), 255*noise(bg[2]))
    time = getTimeDiff(initial_time)
    textSize(width / 75)
    textAlign(LEFT)
    fill(51)
    if gameover:
        noLoop()
        background(lose_color)
        text('Game Over\nTime: ' + time, board_coords[1].x + board_dims.x / 100, board_coords[0].y + board_dims.y / 100)
        for row in board.grid:
            for tile in row:
                tile.lose_reveal = True
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
    if board.mines_placed:
        robbie.play()
    if robbie.gameover:
        gameover = True
    elif robbie.gameover is None:
        gameover = None

def mousePressed():
    global gameover, initial_time
    if mouseButton == LEFT:
        for r in range(len(board.grid)):
            for c in range(len(board.grid[r])):
                if board.grid[r][c].isHovered():
                    if not board.mines_placed:
                        initial_time = millis()
                        robbie.play(r, c)
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
                    
