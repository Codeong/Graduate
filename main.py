import sys

import pygame

# Initialise pygame modules
pygame.init()

HEIGHT = 960
WIDTH = 1152

# Setting clock for frequency of updates in game loop
clock = pygame.time.Clock()

# Window resolution configuration
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Rect list to define barriers
rects = []

MAP = [
    '####################################',
    '#                                  #',
    '#                                  #',
    '#                         #####    #',
    '#                                  #',
    '#  #######                         #',
    '#                                  #',
    '#                  #####           #',
    '#                                  #',
    '#                                  #',
    '#                                  #',
    '#      ######              #####   #',
    '#                                  #',
    '#                                  #',
    '#                                  #',
    '#               #####              #',
    '#                                  #',
    '#                                  #',
    '#                                  #',
    '#       #######                  ###',
    '#                           ##     #',
    '#                     ##           #',
    '######                             #',
    '#                 ##               #',
    '#                                  #',
    '#             ##                   #',
    '#                                  #',
    '#                                  #',
    '#         ##                       #',
    '####################################',
]

for y, row in enumerate(MAP):
    for x, block in enumerate(row):
        if block == "#":
            # Appending Rect object to rect list to blit barrier tiles and check collisions further on
            rects.append(pygame.Rect(x * 32, y * 32, 32, 32))


class Player:
    def __init__(self):
        self.rect = pygame.Rect(128, 128, self.WIDTH, self.HEIGHT)
        
        # Size of player sprite
        self.WIDTH, self.HEIGHT = 64, 64

        self.velocity = 0

        # Physics constants
        self.GRAVITY = 2
        self.TERMINAL_VELOCITY = 48
        self.SPEED = 8

    def check_col(self, dx, dy):
        # Create hitboxes for horizontal and vertical movement
        horizontal_hitbox = pygame.Rect(
            self.rect.x + dx, self.rect.y, self.WIDTH, self.HEIGHT)
        vertical_hitbox = pygame.Rect(
            self.rect.x, self.rect.y + dy, self.WIDTH, self.HEIGHT)

        for tile in rects:
            # Check if the tile collides with the horizontal hitbox
            if tile.colliderect(horizontal_hitbox):
                # Makes the player unable to move on the x-axis
                dx = 0

            # Check if the tile collides with the vertical hitbox
            if tile.colliderect(vertical_hitbox):
                # Checks if player is falling
                if dy < 0:
                    # Adjusts bottom of player to top of the tile collided with
                    dy = tile.bottom - self.rect.top
                    self.velocity = 1

                # Checks if player is jumping
                elif dy > 0:
                    # Adjusts top of player to bottom of the tile collided with
                    dy = tile.top - self.rect.bottom
                    self.velocity = 0

                
        return dx, dy

    def move(self):
        dx, dy = 0, 0

        if keys[pygame.K_SPACE] and self.velocity == 0:
            self.velocity -= 21

        # Apply gravity and limit velocity to terminal velocity
        self.velocity += self.GRAVITY

        if self.velocity > self.TERMINAL_VELOCITY:
            self.velocity = self.TERMINAL_VELOCITY

        dy += self.velocity

        # Check for horizontal movement input
        if keys[pygame.K_a]:
            dx -= self.SPEED

        elif keys[pygame.K_d]:
            dx += self.SPEED

        # Check for collisions and adjust movement accordingly
        dx, dy = self.check_col(dx, dy)

        self.rect.mve_ip(dx, dy)

    def draw(self):
        # Draw temporary player sprite
        pygame.draw.rect(win, (0, 0, 255), self.rect)

    def update(self):
        self.move()
        self.draw()


player = Player()

while True:
    # Register keyboard inputs
    keys = pygame.key.get_pressed()

    win.fill((100, 131, 176))  # Sky blue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calls the update method of the player
    player.update()

    # Render tiles
    for rect in rects:
        pygame.draw.rect(win, (60, 60, 60), rect)
    pygame.display.flip()

    # Limits FPS to 60
    clock.tick(60)