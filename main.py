import sys

import pygame

pygame.init()

HEIGHT = 960
WIDTH = 1152

GRAVITY = 1.5
TERMINAL_VELOCITY = 40
JUMP_POWER = 23
MAX_SPEED = 8

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

# Set clock for frequency of updates in game loop.
clock = pygame.time.Clock()

# Configurate window resolution.
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Define list to contain barriers.
rects = []
for y, row in enumerate(MAP):
    for x, block in enumerate(row):
        if block == "#":
            # Appending Rect object to rect list to blit barrier
            # tiles and check collisions further on.
            rects.append(pygame.Rect(x * 32, y * 32, 32, 32))


class Player:
    """Object representing the player"""

    def __init__(self):
        self.rect = pygame.Rect(128, 128, 64, 64)

        self.y_velocity = 0

    def _check_col(self, dx: int, dy: int) -> tuple:
        # Check if the player would collide if it moved the specified
        # direction. If it collides with the level, then it will
        # return a modified dx and dy to account for the collision,
        # else it will return dx and dy unchanged.

        # Create hitboxes for horizontal and vertical movement.
        horizontal_hitbox = pygame.Rect(self.rect.x + dx, self.rect.y,
                                        self.rect.width, self.rect.height)
        vertical_hitbox = pygame.Rect(self.rect.x, self.rect.y + dy,
                                      self.rect.width, self.rect.height)

        for tile in rects:
            # Check if the tile collides with the horizontal
            # hitbox.
            if tile.colliderect(horizontal_hitbox):
                # Make the player unable to move horizontally.
                dx = 0

            # Check if the tile collides with the vertical
            # hitbox.
            if tile.colliderect(vertical_hitbox):
                # Check if player is falling.
                if dy < 0:
                    # Move bottom of player to top of the
                    # tile collided with.
                    dy = tile.bottom - self.rect.top
                    self.y_velocity = 1

                # Check if player has upwards velocity.
                elif dy > 0:
                    # Move top of player to bottom of the
                    # tile collided with.
                    dy = tile.top - self.rect.bottom
                    self.y_velocity = 0

        return dx, dy

    def _move(self):
        # Detect if the user is pressing movement keys and move
        # accordingly. Also apply gravity.

        dx, dy = 0, 0

        if ((keys[pygame.K_SPACE] or keys[pygame.K_w])
                and self.y_velocity == 0):
            self.y_velocity -= JUMP_POWER

        # Apply gravity and limit velocity to terminal velocity.
        self.y_velocity += GRAVITY
        if self.y_velocity > TERMINAL_VELOCITY:
            self.y_velocity = TERMINAL_VELOCITY
        dy += self.y_velocity

        # Check for horizontal movement input.
        if keys[pygame.K_a]:
            dx -= MAX_SPEED

        elif keys[pygame.K_d]:
            dx += MAX_SPEED

        # Check for collisions and adjust movement accordingly.
        dx, dy = self._check_col(dx, dy)

        self.rect.move_ip(dx, dy)

    def _draw(self, surface: pygame.Surface):
        # Draw placeholder player sprite.
        pygame.draw.rect(surface, (0, 0, 255), self.rect)

    def update(self, surface: pygame.Surface):
        """Updates the player for the frame.
        
        Arguments:
        surface -- the pygame.Surface to draw onto
        """
        self._move()
        self._draw(surface)


player = Player()

while True:
    # Register keyboard inputs.
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((100, 131, 176))
    player.update(win)
    for rect in rects:
        pygame.draw.rect(win, (60, 60, 60), rect)
    pygame.display.flip()

    clock.tick(60)
