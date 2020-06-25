import os
import time
import random
import pygame
import assets

pygame.init()
assets.Assets.load()
#screen
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# ICON = pygame.image.load("assets/images/icon.png")
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(assets.Assets.ICON)
FONT = assets.Assets.FONT


class Colors:
    """Color palette."""

    COTTON_PINK = (255,231,253)
    LILAC = (234,222,253)
    PINK = (227, 69, 179)
    PURPLE = (162,77,178)
    BLUE = (39,93,133)

BLOCKERS_POSITION = 450

class SpaceShip():
    """Player ship."""
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = assets.Assets.SPACE_SHIP
        self.bullet_image = assets.Assets.SHIP_BULLET
        self.bullets = []
        # self.rect = self.image.get_rect(topleft=(375, 540))
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.ship_image)

    def draw(self, screen):
        screen.blit(self.ship_image, (self.x, self.y))

    def get_width(self):
        return self.ship_image.get_width()

class Enemy():
    """Player enemies."""

    ENEMIES_MAP = {
                    "pink": (assets.Assets.ENEMY1),
                    "blue": (assets.Assets.ENEMY2)
                    }

    def __init__(self, x, y, color, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.enemy_image = self.ENEMIES_MAP[color]
        self.bullet_image = assets.Assets.ENEMY_BULLET
        self.bullets = []
        # self.rect = self.image.get_rect(topleft=(375, 540))
        self.mask = pygame.mask.from_surface(self.enemy_image)

    def draw(self, screen):
        screen.blit(self.enemy_image, (self.x, self.y))

    def move(self, speed, direction):
        self.direction = direction
        while self.x + self.enemy_image.get_width() >= WIDTH:
            self.x += speed*direction
        self.y += speed

        while self.x <0:
            self.x -= speed * direction


        #self.x -= speed

class Blocker():
    """Blocker behinde which player can hide from enemies."""
    def __init__(self, size, color, x, y):
        self.height = size/2
        self.width = size
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(self.image)



    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)



def main():
    running = True
    FPS = 60
    score = 0
    lives = 3
    clock = pygame.time.Clock()
    player = SpaceShip(450, 500)

    enemies = []
    wave_length = 5
    enemy_speed = 1
    enemy_direction = 1

    blocker1 = Blocker(100, Colors.LILAC, 100, 450)
    blocker2 = Blocker(100, Colors.PURPLE, 350, 450)
    blocker3 = Blocker(100, Colors.LILAC, 600, 450)

    lost = False
    lost_count = 0


    def draw_background():
        """Drawing background of a game."""
        SCREEN.blit(assets.Assets.BACKGROUND,(0,0))
        lives_label = FONT.render(f"Lives: {lives}",1, Colors.COTTON_PINK)
        score_label = FONT.render(f"Score: {score}",1, Colors.PINK)

        SCREEN.blit(lives_label, (10,10))
        SCREEN.blit(score_label, (WIDTH - lives_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(SCREEN)

        blocker1.draw(SCREEN)
        blocker2.draw(SCREEN)
        blocker3.draw(SCREEN)

        player.draw(SCREEN)

        if lost:
            lost_label = FONT.render("GAME OVER", 1, Colors.PURPLE)
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while running:
        clock.tick(FPS)
        draw_background()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                running = False
            else:
                continue

        if len(enemies) == 0:
            score += 100
            wave_length += 5
            enemy_speed += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["pink", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()



        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player.speed > 0:
            player.x -= player.speed
        if keys[pygame.K_RIGHT] and player.x + player.speed + player.get_width() < WIDTH:
            player.x += player.speed

        for enemy in enemies[:]:
            enemy.move(enemy_speed, enemy_direction)

#  [inicjalizacja bibliotek zewnętrznych]
   # [tworzenie obiektów odpowiednich klas]
   # [wywołanie funkcji lub metody wprawiającej te obiekty w ruch]
   # [sprzątanie]
    draw_background()
def main_menu():
    run = True
    while run:
        SCREEN.blit(assets.Assets.BACKGROUND, (0,0))
        title_label = FONT.render("Press START to begin", 1, Colors.PURPLE)
        start = FONT.render("START", 1, Colors.PINK)
        SCREEN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 250))
        SCREEN.blit(start, (WIDTH / 2 - start.get_width()/ 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                main()
    pygame.quit()

main_menu()