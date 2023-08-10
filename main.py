import os.path
import sys

import pygame

from spritesheet import Spritesheet

pygame.init()

HEIGHT = 960
WIDTH = 1152

GRAVITY = 1.5
TERMINAL_VELOCITY = 40
JUMP_POWER = 23
MAX_SPEED = 8
ACCELERATION = 1
FRICTION = 0.7

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
        spritesheet = Spritesheet(os.path.join("assets", "player.png"))
        self.moving_sprites = {
            "left": [
                spritesheet.parse_sprite("player" + str(i) + ".png")
                for i in range(7)
            ],
            "right": [
                pygame.transform.flip(
                    spritesheet.parse_sprite("player" + str(i) + ".png"), True,
                    False) for i in range(7)
            ]
        }
        self.step_index = 0
        self.counter = 0
        self.direction = "left"

        self.width, self.height = self.moving_sprites["left"][0].get_size()

        self.rect = pygame.Rect(128, 128, self.width, self.height)

        self.y_velocity = 0
        self.x_velocity = 0

    def _check_col(self, dx: int, dy: int) -> tuple:
        # Check if the player would collide if it moved the specified
        # direction. If it collides with the level, then it will
        # return a modified dx and dy to account for the collision,
        # else it will return dx and dy unchanged.

        # Create hitboxes for horizontal and vertical movement.
        horizontal_hitbox = pygame.Rect(self.rect.x + dx, self.rect.y,
                                        self.width, self.height)
        vertical_hitbox = pygame.Rect(self.rect.x, self.rect.y + dy,
                                      self.width, self.height)

        for tile in rects:
            # Check if the tile collides with the horizontal
            # hitbox.
            if tile.colliderect(horizontal_hitbox):
                # Make the player unable to move horizontally.
                dx = 0
                self.x_velocity = 0

            # Check if the tile collides with the vertical
            # hitbox.
            if tile.colliderect(vertical_hitbox):
                # Check if player is falling.
                if dy < 0:
                    # Move bottom of player to top of the
                    # tile collided with.
                    dy = tile.bottom - self.rect.top
                    self.y_velocity = 2

                # Check if player has upwards velocity.
                elif dy > 0:
                    # Move top of player to bottom of the
                    # tile collided with.
                    dy = tile.top - self.rect.bottom
                    self.y_velocity = 0

        return dx, dy

    def _move(self):
        # Detect if the user is pressing movement keys and move
        # accordingly. Also apply gravity and friction.

        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.y_velocity == 0:
            self.y_velocity -= JUMP_POWER

        # Apply gravity and limit velocity to terminal velocity.
        self.y_velocity += GRAVITY
        if self.y_velocity > TERMINAL_VELOCITY:
            self.y_velocity = TERMINAL_VELOCITY

        # Check for horizontal movement input.
        if keys[pygame.K_a]:
            self._update_sprite("right")
            self.x_velocity -= ACCELERATION
        elif keys[pygame.K_d]:
            self._update_sprite("left")
            self.x_velocity += ACCELERATION
        else:
            self.moving = False
            if self.x_velocity:
                # Apply friction.
                self.x_velocity -= self.x_velocity // abs(
                    self.x_velocity) * FRICTION

        # Set x_velocity to the MAX_SPEED if it is too high.
        if abs(self.x_velocity) > MAX_SPEED:
            self.x_velocity = self.x_velocity // abs(
                self.x_velocity) * MAX_SPEED

        dx, dy = self._check_col(self.x_velocity, self.y_velocity)

        self.rect.move_ip(dx, dy)

    def _update_sprite(self, direction: str):
        # Change the direction that the images is facing if needed.
        self.direction = direction
        self.moving = True

        # Change the frame of the moving animation every 4 frames.
        if self.counter % 4 == 0:
            self.step_index += 1

    def _draw(self, surface: pygame.Surface):
        # Draw the player onto the surface.

        # Check if player is moving but not jumping.
        if self.y_velocity >= 0 and self.x_velocity and self.moving:
            # Calculate what image should be drawn.
            image_index = 1 + self.step_index % (
                len(self.moving_sprites[self.direction]) - 1)

        else:
            # Set the frame to stationary if the player is not moving.
            image_index = 0

        # Draw the player.
        win.blit(self.moving_sprites[self.direction][image_index],
                 (self.rect.x, self.rect.y))

    def update(self, surface: pygame.Surface):
        """Updates the player for the frame.
        
        Arguments:
        surface -- the pygame.Surface to draw onto
        """
        self.counter += 1
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

    # Render tiles.
    win.fill((100, 131, 176))
    player.update(win)
    for rect in rects:
        pygame.draw.rect(win, (60, 60, 60), rect)
    pygame.display.flip()

    clock.tick(60)
