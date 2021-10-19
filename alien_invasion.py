import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
#Overall class to manage game assets and behavior
    def __init__(self):
        #Initialize the game, and create game resources:
        pygame.init()

        #Instance of settings:
        self.settings = Settings()

        #Create a display window on which we'll draw all the game's graphical elements:
            #Assign it to self.screen so it will be availabe in all methods in the class
            #object we assigned to self.screen is a SURFACE (part of the screen where a game element can be displayed (an element can be like an alien or a ship))
        #sets size to fullscreen
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        #instance of Ship
        self.ship = Ship(self)
        #group of bullets (behaves like a list)
        self.bullets = pygame.sprite.Group()

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
            #updates bullet locations:
            self.bullets.update()
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
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        '''Respond to keyprssees.'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #press Q to quit game:
        elif event.key == pygame.K_q:
            sys.exit()
        #press spacebar to fire bullet
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event): 
        '''Respond to key releases.'''
        if event.key == pygame.K_RIGHT:
            #Move the ship to the right:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                
    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group'''
        #check the length of bullets -> if less than 3, we create a new bulleet
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            #make an instance of bullet
                #add adds instance to group (similar to append)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''Update position of bullets and get rid of old bullets'''
        #update bullet positions
        #Get rid of bullets that have disappeared:
            #use the copy() method to set up the for loop which enables us to modify bullets inside the loop
                #have to loop over a copy of the group because we can't remove items from a list of group within for loop
        for bullet in self.bullets.copy():
            #checks if bullet has disappeared off the top of the screen
            if bullet.rect.bottom <= 0:
                #if it has disappeared, we remove it
                self.bullets.remove(bullet) 

    def _update_screen(self):
        #redraw the screen during each pass through the loop:
        self.screen.fill(self.settings.bg_color)

        #draw the ship on the screen
        self.ship.blitme()

        #sprites method returns a list of all sprites in the group bullet
            #to draw all fired bullets to screen, we loop through the sprites in bullets and call draw_bullet() on each one
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #make the most recently drawn screen visible:
            #draws an empty screen on each pass through the while loop
            #basically continually updates the display to create the illusion of smooth movement
        pygame.display.flip()

if __name__ == '__main__':
    #GAME INSTANCE:
    ai = AlienInvasion()
    ai.run_game()



'''STOPPED BEFORE "ADJUSTING THE SHIP'S SPEED ON PAGE 240"'''