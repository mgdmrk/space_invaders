import random
import math
import pygame
import assets

pygame.init()
assets.Assets.load()
#screen
WIDTH, HEIGHT = 800, 600 #display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(assets.Assets.ICON)
FONT = assets.Assets.FONT


class Colors:
    """Color palette."""

    COTTON_PINK = (255, 231, 253)
    LILAC = (234, 222, 253)
    PINK = (227, 69, 179)
    PURPLE = (162, 77, 178)
    BLUE = (39, 93, 133)


class Bullet:
    """Player ship and enemies can hit each other with Bullet object."""
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        """ Drawing object on the screen."""
        window.blit(self.image, (self.x, self.y))

    def move(self, speed):
        """Moving bullets on the screen by its y axis."""
        self.y += speed

    def off_screen(self, height):
        """Checking if bullet is off the screen."""
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        """Checking if bullet has collided with enemy or player."""
        distance = math.sqrt(math.pow(obj.x-self.x, 2) + (math.pow(obj.y-self.y, 2)))

        if distance < 27:
            return True
        else:
            return False

class SpaceShip():
    """Player's ship."""

    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.ship_image = assets.Assets.SPACE_SHIP
        self.bullets = []
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.cool_down_counter = 0
        self.bullet_image = assets.Assets.SHIP_BULLET

    def draw(self, screen):
        """ Drawing objects on the screen."""
        screen.blit(self.ship_image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)
        self.healthbar(screen)

    def healthbar(self, screen):
        """Showing health of the player - when the health has ended the game is over """
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y + self.ship_image.get_height() + 10,
                                               self.ship_image.get_width(), 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + self.ship_image.get_height() + 10,
                                               self.ship_image.get_width() * (self.health/self.max_health), 10))

    def move_bullets(self, speed, objs, score):
        """Moving bullets of the player."""
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(speed)

            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        score += 10
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
        return score


    def shoot(self):
        """Adding Bullet object to the list."""
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x, self.y, self.bullet_image)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()

class Enemy():
    """Creats player's enemies."""

    ENEMIES_MAP = {
        "pink": (assets.Assets.ENEMY1),
        "blue": (assets.Assets.ENEMY2)
    }
    COOLDOWN = 30

    def __init__(self, x, y, color, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.enemy_image = self.ENEMIES_MAP[color]
        self.bullets = []
        self.mask = pygame.mask.from_surface(self.enemy_image)
        self.cool_down_counter = 0
        self.bullet_image = assets.Assets.ENEMY_BULLET

    def draw(self, screen):
        """ Drawing objects on the screen."""
        screen.blit(self.enemy_image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)

    def move(self, speed):
        """Moves enemy down the screen."""
        self.y += speed

    def move_bullets(self, speed, obj):
        """Moving bullets of enemies - its hurt the player health."""
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(speed)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)

    def shoot(self):
        """Adding Bullet object to the list."""
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x-20, self.y, self.bullet_image)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1


    def get_width(self):
        return self.enemy_image.get_width()

    def get_height(self):
        return self.enemy_image.get_height()


def collide(obj1, obj2):
    """Checks if objects have collided."""
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def main():
    running = True
    frames_per_second = 60
    score = 0
    lives = 3

    player = SpaceShip(450, 500)
    ship_speed = 5

    enemies = []
    wave_length = 0
    enemy_speed = 1

    bullet_speed = 5

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0


    def draw_background():
        """Drawing background of a game."""
        SCREEN.blit(assets.Assets.BACKGROUND, (0, 0))
        lives_label = FONT.render(f"Lives: {lives}", 1, Colors.COTTON_PINK)
        score_label = FONT.render(f"Score: {score}", 1, Colors.PINK)

        SCREEN.blit(lives_label, (10, 10))
        SCREEN.blit(score_label, (WIDTH - lives_label.get_width() - 100, 10))

        for enemy in enemies:
            enemy.draw(SCREEN)

        player.draw(SCREEN)

        if lost:
            lost_label = FONT.render("GAME OVER", 1, Colors.PURPLE)
            SCREEN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while running:

        clock.tick(frames_per_second)
        draw_background()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > frames_per_second * 3:
                running = False
            else:
                continue

        if len(enemies) == 0:
            wave_length += 5
            enemy_speed += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100),
                              random.choice(["pink", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()



        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - ship_speed > 0:
            player.x -= ship_speed
        if keys[pygame.K_RIGHT] and player.x + ship_speed + player.get_width() < WIDTH:
            player.x += ship_speed
        if keys[pygame.K_SPACE]:
            player.shoot()


        for enemy in enemies[:]:
            enemy.move(enemy_speed)
            enemy.move_bullets(bullet_speed, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_bullets(-bullet_speed, enemies, score)
        score = player.move_bullets(-bullet_speed, enemies, score)





def main_menu():
    run = True
    while run:
        SCREEN.blit(assets.Assets.BACKGROUND, (0, 0))
        title_label = FONT.render("Press START to begin", 1, Colors.PURPLE)
        start = FONT.render("START", 1, Colors.PINK)
        SCREEN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 250))
        SCREEN.blit(start, (WIDTH / 2 - start.get_width()/ 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
