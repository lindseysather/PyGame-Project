import pygame

class Ship:

    #__init__ method uses ai_game to reference the current instance of the AlienInvasion class
        #gives Ship access to all the game resources defined in AlienInvasion 
    def __init__(self, ai_game):
        #Initalize the ship and set its starting position
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship and gets its rect (rectangle):
            #python treats all game elements like recatanlges - more efficient
            #load image and then get_rect() to access the ship surface's rect attibure so we can use it later to place the ship
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen:
            #in pygame the origin (0,0) is the top-left corner of the screen; the bottom right is (1200,800)
        self.rect.midbottom = self.screen_rect.midbottom

        #Movement flag:
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #update the ship's position based on the movement flag
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

        #draws the image to the screen:
    def blitme(self):
        #draw the ship at its current location:
        self.screen.blit(self.image, self.rect)


