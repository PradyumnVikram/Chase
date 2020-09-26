import pygame
import random
import os

pygame.init()

WIDTH = 500
HEIGHT = 500

root = os.path.join(os.path.dirname(__file__), 'data')

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chase!')

STAT_FONT = pygame.font.SysFont('comicsans', 30)

police_imgs = [pygame.image.load(os.path.join(root, 'Police_animation', '{}.png'.format(i + 1))) for i in range(3)]
main_img = pygame.image.load(os.path.join(root, 'Audi.png'))
bg = pygame.transform.scale(pygame.image.load(os.path.join(root, 'bg.png')), (WIDTH, HEIGHT))
intro_bg = pygame.transform.scale(pygame.image.load(os.path.join(root, 'intro_bg.png')), (WIDTH, HEIGHT))

ouch = pygame.image.load(os.path.join(root, 'ouch.png'))


class Car:

    def __init__(self, lanes, lane):
        self.lanes = lanes
        self.lane = lane
        self.x, self.y = self.lanes[self.lane]
        self.img = pygame.transform.flip(pygame.transform.scale(main_img, (150, 150)), True, True)
        self.vel = 10

    def draw(self, window):
        self.x, self.y = self.lanes[self.lane]
        window.blit(self.img, (self.x, self.y))


class Player(Car):
    def __init__(self, lanes, lane):
        super().__init__(lanes, lane)

    def move(self, key):
        if key == 'R':
            if self.lane + 1 <= 3:
                self.lane += 1
        elif key == 'L':
            if self.lane - 1 >= 1:
                self.lane -= 1

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Base:
    def __init__(self, x):
        self.base_height = bg.get_height()
        self.img = bg
        self.vel = 10
        self.y1 = 0
        self.y2 = self.base_height
        self.x = x

    def move(self):
        self.y1 -= self.vel
        self.y2 -= self.vel

        if self.y1 + self.base_height < 0:
            self.y1 = self.y2 + self.base_height

        if self.y2 + self.base_height < 0:
            self.y2 = self.y1 + self.base_height

    def draw(self, window):
        window.blit(self.img, (int(self.x), int(self.y1)))
        window.blit(self.img, (int(self.x), int(self.y2)))


class Police:
    def __init__(self, lanes, lane):
        self.lanes = lanes
        self.lane = lane
        self.x, _ = self.lanes[self.lane]
        self.vel = random.randint(5, 10)
        self.ind = 0
        self.imgs = police_imgs
        self.img = self.imgs[self.ind]
        self.y = -self.imgs[0].get_height()

    def move(self):
        self.y += self.vel

    def draw(self, window):
        self.img = self.imgs[self.ind]
        window.blit(pygame.transform.flip(pygame.transform.scale(self.img, (150, 150)), True, True), (self.x, self.y))
        self.ind += 1
        if self.ind == 3:
            self.ind = 0

    def collide(self, player):
        player_mask = player.get_mask()
        mask = pygame.mask.from_surface(self.img)
        offset = (self.x - player.x, self.y - round(player.y))
        point = player_mask.overlap(mask, offset)

        if point:
            return True
        return False


def redraw_window(WIN, player, bgObj, fleet, flag, score):
    bgObj.draw(WIN)
    player.draw(WIN)
    for car in fleet:
        car.draw(WIN)
    if flag:
        WIN.blit(ouch, (player.x - 100, player.y - 100))
    text = STAT_FONT.render('Score:  ' + str(score), 1, (10, 10, 10))
    WIN.blit(text, (WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()


def main():
    flag = False
    score = 0
    lanes = {1: (5, HEIGHT - main_img.get_height() + 70),
             2: (125, HEIGHT - main_img.get_height() + 70),
             3: (250, HEIGHT - main_img.get_height() + 70)}
    player = Player(lanes, 3)
    run = True
    bgObj = Base(0)
    clock = pygame.time.Clock()
    opponent = Police(lanes, random.randint(1, 3))
    fleet = [opponent]
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not flag:
            clock.tick(60)
            score += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    player.move('R')
                if keys[pygame.K_LEFT]:
                    player.move('L')
            for ind, car in enumerate(fleet):
                car.move()
                if car.collide(player) and car.lane == player.lane:
                    if player.y - car.y <= 100:
                        flag = True
                if car.y >= HEIGHT:
                    fleet.pop(ind)
            if len(fleet) == 0:
                fleet.append(Police(lanes, random.randint(1, 3)))

            bgObj.move()
            redraw_window(win, player, bgObj, fleet, flag, score)


def main_menu():
    run = True
    title_font = pygame.font.SysFont('comicsans', 60)

    while run:
        win.fill((200, 200, 200))
        win.blit(intro_bg, (0, 0))
        intro = title_font.render('Press SPACE to start!', 1, (255, 255, 255))
        win.blit(intro, (int(WIDTH / 2 - intro.get_width() / 2) + 10, 240))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                main()
    pygame.quit()


main_menu()
