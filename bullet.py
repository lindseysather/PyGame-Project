import pygame
#when you use sprites, you can group related elements in your game and act on all the grouped elements at once
#group behaves like a list 
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''A class to manage bullets fired from the ship'''

    def __init__(self, ai_game):
        '''Create a bullet object at the ship's current position'''
        #inherits the current instance of AlienInvasion, and we call super to inherit properly from Sprite
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0,0) and then set correct position:
            #don't have an image so rect builds something from scratch 
            #takes width and height from settings
            #initializes position at 0,0 but we'll move it in the next line
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        #links bullet location with the ship (midtop puts it at the top of the ship)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        '''Move the bullet up the screen'''
        #Update the decimal position of the bullet
            #position corresponds to a decreasing y coordinate value
        self.y -= self.settings.bullet_speed
        #Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draw the bullet to the screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)