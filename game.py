import pygame
import os
import random

pygame.init()
fps = 80
HP = 5
Clock = 0
Score = 0
Life = True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


class M(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('p.png'), (50, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = M.image
        self.rect = self.image.get_rect()
        self.rect.x = 475
        self.rect.y = 475

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.rect.y = max(75, self.rect.y - 100)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.rect.y = min(875, self.rect.y + 100)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.rect.x = max(75, self.rect.x - 100)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.rect.x = min(875, self.rect.x + 100)


class Enemy1(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("red.png"), (24, 24))

    def __init__(self, group):
        super().__init__(group)
        self.image = Enemy1.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = random.randrange(1, 10) * 100 - 12

    def update(self):
        self.rect = self.rect.move(min(11, 3 + (Score // 12)), 0)


class Enemy2(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("red.png"), (24, 24))

    def __init__(self, group):
        super().__init__(group)
        self.image = Enemy2.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, 10) * 100 - 12
        self.rect.y = 6

    def update(self):
        self.rect = self.rect.move(0, min(11, 3 + (Score // 12)))


class Wall1(pygame.sprite.Sprite):
    image = load_image("wall1.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Wall1.image


class Wall2(pygame.sprite.Sprite):
    image = load_image("wall2.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Wall2.image


def show_int():
    font = pygame.font.Font(None, 50)
    hp = 'жизни ' + str(HP)
    text1 = font.render(hp, 1, (255, 0, 0))
    screen.blit(text1, (20, 20))
    ochki = 'очки ' + str(Score)
    text2 = font.render(ochki, 1, (255, 0, 0))
    screen.blit(text2, (850, 20))


def is_life():
    global Life
    if HP < 1:
        Life = False


def collaid(sprite, group1, group2):
    global HP
    if pygame.sprite.spritecollide(sprite, group1, True):
        HP = HP - 1
    if pygame.sprite.spritecollide(sprite, group2, True):
        HP = HP - 1


def wall(p, e1, e2, w1, w2, w3, w4, p_g):
    global Score
    deid = pygame.sprite.spritecollide(w1, e1, True)
    if deid:
        Score += len(deid)
        deid = []
    deid1 = pygame.sprite.spritecollide(w4, e2, True)
    if deid1:
        Score += len(deid1)
        deid1 = []


def spawn():
    global Clock
    Clock += min(30, 8 + (Score // 12))
    if Clock > 600:
        for i in range(min(6, 3 + (Score // 12))):
            saiori1 = Enemy1(enemys1)

        for j in range(min(6, 3 + (Score // 12))):
            saiori2 = Enemy2(enemys2)
        Clock = 0


background_image = load_image("back1.png")
background_image_lose = load_image("back_lose.png")
clock = pygame.time.Clock()
size = width, height = 1000, 1000

player = pygame.sprite.Group()

monk = M(player)

enemys1 = pygame.sprite.Group()
enemys2 = pygame.sprite.Group()
wall_1 = pygame.sprite.Group()

wall1 = Wall1(wall_1)
wall1.rect = monk.image.get_rect()
wall1.rect.x = 995
wall1.rect.y = 0
wall1.rect.h = 1000
wall1.rect.w = 10

wall2 = Wall1(wall_1)
wall2.rect = monk.image.get_rect()
wall2.rect.x = 0
wall2.rect.y = 0

wall3 = Wall2(wall_1)
wall3.rect = monk.image.get_rect()
wall3.rect.x = 0
wall3.rect.y = 0

wall4 = Wall2(wall_1)
wall4.rect = monk.image.get_rect()
wall4.rect.x = 0
wall4.rect.y = 995
wall4.rect.h = 10
wall4.rect.w = 1000

screen = pygame.display.set_mode(size)
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if Life == True:
            monk.event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 900 > event.pos[0] > 260 and 950 > event.pos[1] > 800:
                    Life = True
                    HP = 5
                    Score = 0
                    enemys1.empty()
                    enemys2.empty()
                    monk.rect.x = 475
                    monk.rect.y = 475

    is_life()
    screen.fill((0, 0, 0))

    if Life == True:
        screen.blit(background_image, [0, 0])
        show_int()
        wall(monk, enemys1, enemys2, wall1, wall2, wall3, wall4, player)
        collaid(monk, enemys1, enemys2)
        spawn()
        enemys1.update()
        enemys2.update()
        enemys1.draw(screen)
        enemys2.draw(screen)
        wall_1.draw(screen)
        player.draw(screen)
    else:
        screen.blit(background_image_lose, [0, 0])
        font = pygame.font.Font(None, 100)
        ochki = 'очки ' + str(Score)
        text2 = font.render(ochki, 1, (255, 0, 0))
        screen.blit(text2, (370, 20))

        with open('recordes.txt', 'r', encoding="utf8") as rec1:
            line1 = rec1.read()

        if int(line1) < Score:
            with open('recordes.txt', 'w', encoding="utf8") as rec2:
                rec2.write(str(Score))

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
