import pygame
import random
from settings import *

pygame.init()
pygame.display.set_caption("Maze")

score = 0
window = pygame.display.set_mode((W, H))
box_size = 40
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 35)
 
class GameObject:
    def __init__(self, x, y, size, color, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.speed = speed
 
class Player(GameObject):
    def control(self):
        key_pressed = pygame.key.get_pressed()
        if (key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]) and self.rect.x > 1:
            self.rect.x -= self.speed
            if self.collide():
                self.rect.x += self.speed
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT] and self.rect.x < W - box_size:
            self.rect.x += self.speed
            if self.collide():
                self.rect.x -= self.speed
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
            if self.collide():
                self.rect.y += self.speed
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN] and self.rect.y < H - box_size:
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
        if self.rect.x >= W - box_size or self.rect.x <= 0:
            self.speed *= -1

    def v_pat(self):
        self.rect.y += self.speed
        if self.rect.y >= H - box_size or self.rect.y <= 0:
            self.speed *= -1

box_list = []
empty_list = []
prize_list = []

for y in range(1, (H // box_size) - 1):
    for x in range(1, (W // box_size) - 1):
        if random.randint(0, 2) == 0:
            if x != (W // box_size) // 2 and y != (H // box_size) // 2:
                box = GameObject(x * box_size, y * box_size, box_size, RED, 0)
                box_list.append(box)
            else:
                empty_list.append((x * box_size, y * box_size))
        else:
            empty_list.append((x * box_size, y * box_size))
            
for i in range(0, 11):
    x,y = random.choice(empty_list)
    empty_list.remove((x, y))
    prize = GameObject(x, y, box_size, YELLOW, 0)
    prize_list.append(prize)
 
x,y = random.choice(empty_list)
empty_list.remove((x, y))
player = Player(x, y, box_size, BLUE, 10)


v_enemy = list()

h_enemy1 = Enemy(0, H - box_size, box_size, WHITE, 10)
h_enemy2 = Enemy(0, 0, box_size, WHITE, 10)

v_enemy1 = Enemy(0, 0, box_size, WHITE, 10)
v_enemy2 = Enemy(W - box_size, 0, box_size, WHITE, 10)

cenr_v_enemy = Enemy(W // 2, 0, box_size, WHITE, 10)
cenr_h_enemy = Enemy(0, H // 2, box_size, WHITE, 10)

h_enemies = [h_enemy1, h_enemy2, cenr_h_enemy]
v_enemies = [v_enemy1, v_enemy2, cenr_v_enemy]

run = True
while run:
    for enemy in h_enemies:
        if enemy.rect.colliderect(player.rect):
            run = False
    for enemy in v_enemies:
        if enemy.rect.colliderect(player.rect):
            run = False

    if score >= 11:
        run = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    window.fill(BLACK)

    for box in box_list:
        window.blit(box.image, box.rect)

    for prize in prize_list:
        window.blit(prize.image, prize.rect)

    player.control()
    score_text = font.render('Счёт: ' + str(score), False, GREEN)
    for enemy in h_enemies:
        window.blit(enemy.image, enemy.rect)
        enemy.h_pat()
    for enemy in v_enemies:
        window.blit(enemy.image, enemy.rect)
        enemy.v_pat()
    window.blit(player.image, player.rect)
    window.blit(score_text, (20, 15))
 
    clock.tick(FPS)    
    pygame.display.update()