import json

import pygame

pygame.init()

class Spritesheet:
    """This class cuts up a given spritesheet into its individual images
    using a json file.
    
    Arguments:
    filename -- name of the file. must have be a png
    """

    def __init__(self, filename: str):
        # Initialize the Spritesheet object with the given filename.
        self.filename = filename
        
        # Load the spritesheet image and convert it for more efficient
        # drawing.
        self.sprite_sheet = pygame.image.load(filename).convert()
        
        # Generate the name of the associated json file by replacing
        # "png" with "json".
        self.meta_data = self.filename.replace("png", "json")

        # Open the json file and load its data as a dictionary.
        with open(self.meta_data) as file:
            self.data = json.load(file)

    def _get_sprite(self, x, y, width, height) -> pygame.Surface:
        sprite = pygame.Surface((width, height))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return sprite

    def parse_sprite(self, name: str) -> pygame.Surface:
        """Extract a frame from the spritesheet given the name

        Arguments:
        name -- the frame's name

        Returns the frame
        """
        # Retrieve the frame information for a specific sprite from the
        # json data.
        sprite = self.data["frames"][name]["frame"]
        
        # Get the sprite using the frame information obtained from the
        # json data.
        return self._get_sprite(sprite["x"], sprite["y"], sprite["w"],
                                sprite["h"])
