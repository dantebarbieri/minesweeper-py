bg_colors = (color(24, 82, 82),
             color(44, 82, 44),
             color(82, 82, 24),
             color(82, 24, 24),
             color(82, 12, 12),
             color(51, 51, 51),
             color(24, 24, 24),
             color (0, 0, 0))
bomb_color = color(102)
bombbg_color = color(255, 188, 188)
flag_color = color(255, 255, 130)
flagbg_color = color(188, 188, 255)
hovered_color = color(255, 201, 255)
hidden_color = color(201)
revealed_color = color(51)
text_color = color(201)

class Tile:
    def __init__(self, pos, dim):
        self.pos = pos.copy()
        self.dim = dim.copy()
        self.revealed = False
        self.is_bomb = False
        self.flagged = None
        self.number = 0
        self.flag_count = 0
    
    def show(self):
        if self.revealed:
            if self.is_bomb:
                fill(bombbg_color)
            elif self.number > 0:
                fill(bg_colors[self.number - 1])
            else:
                fill(revealed_color)
        else:
            if self.isHovered():
                fill(hovered_color)
            elif self.flagged is not None:
                fill(flagbg_color)
            else:
                fill(hidden_color)
        rect(self.pos.x, self.pos.y, self.dim.x, self.dim.y, self.dim.z)
        if self.revealed:
            if self.is_bomb:
                fill(bomb_color)
                circle(self.pos.x + self.dim.x / 2, self.pos.y + self.dim.y / 2, min(self.dim.x, self.dim.y) / 2)
            elif self.number > 0:
                fill(text_color)
                textSize(self.dim.y / 1.3333333333)
                textAlign(CENTER)
                text(str(self.number), self.pos.x + self.dim.x / 2, self.pos.y + self.dim.y / 1.4)
        else:
            if self.flagged is not None:
                noStroke()
                fill(flag_color)
                rect(self.pos.x + self.dim.x / 10, self.pos.y + self.dim.y / 10, self.dim.x / 10, self.dim.y * 8 / 10, self.dim.z)
                rect(self.pos.x + self.dim.x / 10, self.pos.y + self.dim.y / 10, self.dim.x * 7 / 10, self.dim.y * 4 / 10)
                stroke(0)
                if not self.flagged:
                    textSize(self.dim.y / 3.5)
                    textAlign(CENTER)
                    text('?', self.pos.x + self.dim.x * 4 / 5, self.pos.y + self.dim.y * 4 / 5)
                
    
    def reveal(self):
        self.revealed = True
        f = self.flagged
        self.flagged = None
        return self.number == 0, self.is_bomb, f
    
    def isHovered(self):
        return 0 <= mouseX - self.pos.x <= self.dim.x and 0 <= mouseY - self.pos.y <= self.dim.y
