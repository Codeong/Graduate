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

# Set clock for frequency of updates in game loop.
clock = pygame.time.Clock()

# Configurate window resolution.
win = pygame.display.set_mode((WIDTH, HEIGHT))

room_index = 0


class Scene:
    """Class representing a level or 'room'.
    
    Arguments:
    tilemap -- a list of strings representing the level.
    """

    def __init__(self, tilemap: tuple, image: pygame.Surface = None):
        self.TILESIZE = 32
        self.image = image
        self.rects = self._get_rects(tilemap)
        self.ladder = pygame.image.load(os.path.join("assets", "ladder.png"))
        self.stair = pygame.image.load(os.path.join("assets", "stair.png"))

    def _get_rects(self, tilemap: tuple) -> tuple:
        # Get all the rects from the tilemap

        rects = []
        for y, row in enumerate(tilemap):
            for x, block in enumerate(row):
                if block != " ":
                    boundaries = [
                        "wall", "ladder", "left_stair", "right_stair"
                    ]
                    rects.append(
                        (boundaries[int(block)],
                         pygame.Rect(x * self.TILESIZE, y * self.TILESIZE,
                                     self.TILESIZE, self.TILESIZE)))
        return tuple(rects)

    def draw(self, surface: pygame.Surface):
        """Draws the level.
        
        Arguments:
        suurface -- the pygame.Surface to draw onto
        """
        for tile_type, rect in self.rects:
            match tile_type:
                case "wall":
                    pygame.draw.rect(surface, (60, 60, 60), rect)

                case "ladder":
                    surface.blit(self.ladder, (rect.x, rect.y))

                case "left_stair":
                    surface.blit(self.stair, (rect.x, rect.y))

                case "right_stair":
                    surface.blit(
                        pygame.transform.flip(self.stair, True, False),
                        (rect.x, rect.y))

            # if type == "wall":
            #     pygame.draw.rect(surface, (60, 60, 60), rect)

            # elif type == "ladder":
            #     pygame.blit(ladder, (rect.x, rect.y))

            # else:
            #     pygame.blit(stair, (rect.x, rect.y))


rooms = [
    Scene([
        '000000000000000000000000000000000000',
        '0                                  0',
        '0                0                 0',
        '0               00                 0',
        '0              0 0                 0',
        '0                0                 0',
        '0                0                 0',
        '0                0                 0',
        '0                0                 0',
        '0                0                 0',
        '0                0                 0',
        '0              00000               0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                   ',
        '0                                   ',
        '0                         2         ',
        '0                        20         ',
        '0                       200         ',
        '000000000000000000000000000000000000',
    ]),
    Scene([
        '000000000000000000000000000000000000',
        '0                                  0',
        '0             000000               0',
        '0            0      0              0',
        '0            0      0              0',
        '0                  00              0',
        '0                 00               0',
        '0                00                0',
        '0              00                  0',
        '0             0                    0',
        '0             00000000             0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                   ',
        '0                                   ',
        '0                                   ',
        '0                               0000',
        '0                                   ',
        '                                    ',
        '                                    ',
        '            2   3                   ',
        '           20   03                  ',
        '          200   003                 ',
        '000000000000000000000000000000000000',
    ]),
    Scene([
        '000000000000000000000000000000000000',
        '0                                  0',
        '0            000000                0',
        '0                  0               0',
        '0                   0              0',
        '0                   0              0',
        '0                  0               0',
        '0            000000                0',
        '0                 00               0',
        '0                  00              0',
        '0                   0              0',
        '0                  00              0',
        '0            00   00               0',
        '0             00000                0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '0                                  0',
        '                          1        0',
        '                          1        0',
        '                          1        0',
        '00000000    0000000000000 1        0',
        '                          1        0',
        '                          1        0',
        '                          1        0',
        '                          1        0',
        '                          1        0',
        '                          1        0',
        '000000000000000000000000000000000000',
    ])
]


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

        for tile_type, tile in rooms[room_index].rects:
            if tile_type == "ladder":
                if tile.colliderect(self.rect) and (
                        keys[pygame.K_SPACE]
                        or keys[pygame.K_w]) and self.y_velocity <= 0:
                    self.y_velocity = 0
                    dy = -8

            elif tile_type == "wall":
                if tile.colliderect(horizontal_hitbox):
                    dx = 0
                    self.x_velocity = 0

                if tile.colliderect(vertical_hitbox):
                    if dy < 0:
                        self.y_velocity = 2
                        dy = tile.bottom - self.rect.top
                        return dx, dy

                    elif dy > 0:
                        self.y_velocity = 0
                        dy = tile.top - self.rect.bottom

            elif tile.colliderect(horizontal_hitbox):
                direction = tile_type.split("_")[0]

                if direction == "left":
                    if dx > 0 or tile.colliderect(vertical_hitbox):
                        self.y_velocity = 0
                        dy = tile.top - self.rect.bottom
                        return dx, dy

                else:
                    if dx < 0 or tile.colliderect(vertical_hitbox):
                        self.y_velocity = 0
                        dy = tile.top - self.rect.bottom
                        return dx, dy

                dx = 0

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
        surface.blit(self.moving_sprites[self.direction][image_index],
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

    # Detect if the player is exiting the room.
    if player.rect.right < 0:
        room_index -= 1
        player.rect.left = WIDTH
        player.rect.y -= 5
    if player.rect.left > WIDTH:
        room_index += 1
        player.rect.right = 0
        player.rect.y -= 5

    win.fill((100, 131, 176))
    player.update(win)
    rooms[room_index].draw(win)

    clock.tick(60)
    pygame.display.flip()
