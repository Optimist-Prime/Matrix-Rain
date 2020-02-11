import pygame, sys, random
pygame.init()
 
BLACK = (0, 0, 0)

X = 1400
Y = 900
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Matrix Rain Effect")

symbols = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@%&#%$�")

SIZE = 16
font=pygame.font.Font(None, SIZE)
row_height = SIZE * 0.6
row_width = SIZE

class Column():
    def __init__(self, x):
        self.x = x
        self.clear_and_restart(1000)
        self.add_new_symbol()

    def add_new_symbol(self):
        if 0 < self.y < Y:
            self.list.append(Symbol(self))
        self.y += row_height

    def clear_and_restart(self, start_pos=250):
        pygame.draw.rect(screen, BLACK, (self.x  - row_width//2, 0, row_width, Y), 0)
        self.list = []
        self.y = - random.randint(0, start_pos//row_height) * row_height
        self.fade_age = random.randint(20, 40)
        self.fade_speed = random.randint(2, 5)
        
        if random.random() < 0.99:
            self.color = "green"
        else:
            self.color = "orange"

    def move(self):
        if self.list and self.list[-1].color == BLACK:
            self.clear_and_restart()
        self.add_new_symbol()

    def update(self):
        for symbol in self.list:
            symbol.update()

class Symbol():
    def __init__(self, column):
        self.x = column.x
        self.y = column.y
        self.symbol = random.choice(symbols)
        self.age = 0
        self.fade_age = column.fade_age
        self.fade_speed = column.fade_speed
        
        self.color_function = self.green  # new in this version
        if column.color == "orange":
            self.color_function = self.orange

    def update(self):
        self.draw()
        self.age += 1

    def draw(self):
        self.color_function()
        
        self.surf = font.render(self.symbol, 1, self.color) 
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        screen.blit(self.surf, self.rect)

    def green(self):  # new name in this version
        if self.age < 11:
            self.color = (225-self.age*22, 225-7*self.age, 225-self.age*22)
        elif self.age > self.fade_age:
            self.color = (0, max(0, 155-(self.age-self.fade_age)*self.fade_speed), 0)
        
    def orange(self):  # alternative color
        if self.age < 11:
            self.color = (225-8*self.age, 225-16*self.age, 225-self.age*22)
        elif self.age > self.fade_age:
            self.color = (max(0, 155-(self.age-self.fade_age)*self.fade_speed),
                          max(0, 75-(self.age-self.fade_age)*self.fade_speed//2), 0)
        

col = []
for i in range(1, X//SIZE):
    col.append(Column(i*row_width))

screen.fill(BLACK)

while True:
 
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()

    for c in col:
        c.move()
        c.update()
    pygame.time.wait(20)
    pygame.display.flip()
