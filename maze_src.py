from pygame import *
from random import *

init()
display.set_caption("Maze")
w = 800
h = 800
score = 0
window = display.set_mode((w, h))
box_size = 40
clock = time.Clock()
font = font.SysFont('Arial', 35)
 
class GameObject:
    def __init__(self, x, y, size, color, speed):
        self.rect = Rect(x, y, size, size)
        self.image = Surface((size, size))
        self.image.fill(color)
        self.speed = speed
 
class Player(GameObject):
    def control(self):
        key_pressed = key.get_pressed()
        if (key_pressed[K_a] or key_pressed[K_LEFT]) and self.rect.x > 1:
            self.rect.x -= self.speed
            if self.collide():
                self.rect.x += self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT] and self.rect.x < w - box_size:
            self.rect.x += self.speed
            if self.collide():
                self.rect.x -= self.speed
        if key_pressed[K_w] or key_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
            if self.collide():
                self.rect.y += self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN] and self.rect.y < h - box_size:
            self.rect.y += self.speed
            if self.collide():
                self.rect.y -= self.speed

    def collide(self):
        for box in box_list:
            if self.rect.colliderect(box.rect):
                return True

        for prize in prize_list:
            if self.rect.colliderect(prize.rect):
                prize_list.remove(prize)
                global score
                score += 1

class Enemy(GameObject):
    def h_pat(self):
        self.rect.x += self.speed
        if self.rect.x >= w - box_size or self.rect.x <= 0:
            self.speed *= -1

    def v_pat(self):
        self.rect.y += self.speed
        if self.rect.y >= h - box_size or self.rect.y <= 0:
            self.speed *= -1

box_list = []
empty_list = []
prize_list = []

for y in range(1, (h//box_size)-1):
    for x in range(1, (w//box_size)-1):
        if randint(0, 2) == 0:
            if x != (w // box_size) // 2 and y != (h // box_size) // 2:
                box = GameObject(x*box_size, y*box_size, box_size, (255, 0, 0),0)
                box_list.append(box)
            else:
                empty_list.append((x*box_size, y*box_size))
        else:
            empty_list.append((x*box_size, y*box_size))
            
for i in range(0,11):
    x,y = choice(empty_list)
    empty_list.remove((x,y))
    prize = GameObject(x, y, box_size, (249, 215, 28), 0)
    prize_list.append(prize)
 
x,y = choice(empty_list)
empty_list.remove((x, y))
player = Player(x, y, box_size, (0, 0, 255), 10)

h_enemy1 = Enemy(0, h - box_size, box_size, (255, 255, 255), 10)
h_enemy2 = Enemy(0, 0, box_size, (255, 255, 255), 10)

v_enemy1 = Enemy(0, 0, box_size, (255, 255, 255), 10)
v_enemy2 = Enemy(w - box_size, 0, box_size, (255, 255, 255), 10)

cenr_v_enemy = Enemy(w // 2, 0, box_size, (255, 255, 255), 10)
cenr_h_enemy = Enemy(0, h // 2, box_size, (255, 255, 255), 10)

run = True
while run:
    if score > 11:
        run = False

    for e in event.get():
        if e.type == QUIT:
            run = False

    window.fill((0, 0, 0))

    for box in box_list:
        window.blit(box.image, box.rect)

    for prize in prize_list:
        window.blit(prize.image, prize.rect)

    h_enemy1.h_pat()
    h_enemy2.h_pat()
    v_enemy1.v_pat()
    v_enemy2.v_pat()
    cenr_v_enemy.v_pat()
    cenr_h_enemy.h_pat()
    player.control()
    score_text = font.render('Счёт: ' + str(score), False, (0, 255, 0))
    window.blit(h_enemy1.image, h_enemy1.rect)
    window.blit(h_enemy2.image, h_enemy2.rect)
    window.blit(v_enemy1.image, v_enemy1.rect)
    window.blit(v_enemy2.image, v_enemy2.rect)
    window.blit(cenr_v_enemy.image, cenr_v_enemy.rect)
    window.blit(cenr_h_enemy.image, cenr_h_enemy.rect)
    window.blit(player.image, player.rect)
    window.blit(score_text, (20, 15))
 
    clock.tick(25)    
    display.update()