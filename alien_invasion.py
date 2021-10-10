import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
#Overall class to manage game assets and behavior
    def __init__(self):
        #Initialize the game, and create game resources:
        pygame.init()

        #Instance of settings:
        self.settings = Settings()
        
        #Create a display window on which we'll draw all the game's graphical elements:
            #(1200,8000) is a TUPLE that defines the dimensions of the game window (1200 x 800 pixels)
            #Assign it to self.screen so it will be availabe in all methods in the class
            #object we assigned to self.screen is a SURFACE (part of the screen where a game element can be displayed (an element can be like a n alien or a ship))
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #instance of Ship
        self.ship = Ship(self)

        #set the background color:
        self.bg_color = (230, 230, 230)

    def run_game(self):
        #Start the main loop for the game - will run continually 
        while True:
            #method to simplifiy def run_game() - isolates the loop so you can manage it separatley from other aspects of the gamee
            
            #checks for keyboard events:
            self._check_events()
            #updates ship position:
            self.ship.update()
            #updates the screen:
            self._update_screen()

    def _check_events(self):
        #listens for keyboard and mouse events:
        #EVENT LOOP: manages screen updates. EVENT = action a user performs while eplaying the game (keyboard or mouse movements)
        #pygame.event.get() returns a list of events that have taken place since the last time the function was called
        #any keyboard or mouse event will cause the for loop to run
        for event in pygame.event.get():
            #when a player clicks the game window's closee button:
            if event.type == pygame.QUIT:
                sys.exit()
            #KEYDOWN just means you push down a key 
            elif event.type == pygame.KEYDOWN:
                #K_RIGHT is right arrow key
                if event.type == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True

            #When the player releases a key 
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    #Move the ship to the right:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                
             

    def _update_screen(self):
        #redraw the screen during each pass through the loop:
        self.screen.fill(self.settings.bg_color)

        #draw the ship on the screen
        self.ship.blitme()

        #make the most recently drawn screen visible:
            #draws an empty screen on each pass through the while loop
            #basically continually updates the display to create the illusion of smooth movement
        pygame.display.flip()

if __name__ == '__main__':
    #GAME INSTANCE:
    ai = AlienInvasion()
    ai.run_game()



'''STOPPED BEFORE "ADJUSTING THE SHIP'S SPEED ON PAGE 240"'''