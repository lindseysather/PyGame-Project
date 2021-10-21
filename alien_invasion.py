import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien 

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

        #Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        #Instance to store game stats
        self.stats = GameStats(self)

        #instance of Ship
        self.ship = Ship(self)
        #group of bullets (behaves like a list)
        self.bullets = pygame.sprite.Group()
        #group of aliens
        self.aliens = pygame.sprite.Group()
        #set the background color:
        self.bg_color = (230, 230, 230)

        self._create_fleet()


        #Make the Play button
        self.play_button = Button(self, "Play")


    def run_game(self):
        #Start the main loop for the game - will run continually 
        while True:
            #method to simplifiy def run_game() - isolates the loop so you can manage it separatley from other aspects of the gamee
            
            #checks for keyboard events:
            self._check_events()

            #methods that only do anything if game is active
            if self.stats.game_active:
                #updates ship position:
                self.ship.update()
                #updates bullet locations:
                self._update_bullets()
                #update alien position:
                self._update_aliens()

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                #get_pos() returns a tuple containing the mouse cursor's x- and y-coordinates when the mouse button is clicked
                    #this ensures that you only start the game when you click the play button 
                mouse_pos = pygame.mouse.get_pos()
                #send coordinate values to _check_play_button method 
                self._check_play_button(mouse_pos)
        

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks Play'''
        #collidepoint() checks whether the point of the mouse click overlaps the region defined by the Play button's rect
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #makes play button only able to be clicked while game is inactive
        if button_clicked and not self.stats.game_active:
            #reset game settings (so speed doesn't keep increasing)
            self.settings.initialize_dynamic_settings()
            #reset the game statistics so we can play again after we lose:
            self.stats.reset_stats()
            #game active when Play is clicked 
            self.stats.game_active = True
            #resets score to 0 after starting a new game 
            self.sb.prep_score()
            #update level image
            self.sb.prep_level()
            #show how many ships player has to start with
            self.sb.prep_ships()

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #hide mouse cursor while game is active
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        '''Respond to keypresses.'''
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
        self.bullets.update()

        #Get rid of bullets that have disappeared:
            #use the copy() method to set up the for loop which enables us to modify bullets inside the loop
                #have to loop over a copy of the group because we can't remove items from a list of group within for loop
        for bullet in self.bullets.copy():
            #checks if bullet has disappeared off the top of the screen
            if bullet.rect.bottom <= 0:
                #if it has disappeared, we remove it
                self.bullets.remove(bullet) 

        self._check_bullet_alien_collisions()

    
    def _check_bullet_alien_collisions(self):
        '''Respond to bullet-alien collisions'''
        #Remove any bullets and aliens that hvae collided
        #check for any bullets that have hit aliens
            #sprite.groupcollide() function compares the rects of each element in one group (aliens) with another group (bullets)
            #returns a dictionary containing the bullets and aliens that have collided
            #Key will be a bullet, and the value will be a hit alien
            #True arguments tell Pygame to delete the bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        #if collisions exist, alien's value (50) is added to the score
        if collisions:
            #loops through all values in the dictionary 
            for aliens in collisions.values():
                #calls alien_points from settings (set to 50)
                    #multiplies value of each alien by the number of aliens in eeach list 
                        #remember that each value is a list of aliens hit by a single bullet
                self.stats.score += self.settings.alien_points * len(aliens)
            
            #calls prep_score() definition to create a new image for the updated score
            self.sb.prep_score()

            #need to  call check_high_score() each time an alien is hit after updating the score in _check_bullet_alien_collisions()
            self.sb.check_high_score() 


        #check if aliens group is empty
        if not self.aliens:
            #destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            #increases speed of ship, bullets, and aliens for each level
            self.settings.increase_speed()

            #Increase level
            self.stats.level += 1
            #call prep_level() to make sure new level displays correctly 
            self.sb.prep_level()


    def _update_aliens(self):
        '''Check if the fleet is at an edge, then update the positions of all aliens in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions
        #spritecollideany takes 2 arguments: a sprite and a group
            #looks for any member of the group that has collided with the sprite and stops looping through the group as soon as it finds one member that has collided with the sprite
            #loops through the group aliens and returns the first alien it finds that has collided with ship
            #if no collision occurs, spritecollideany() returns None and the if block won't execute
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
    



    '''CREATE FUNCTIONS'''


    def _create_fleet(self):
        '''Create the fleet of aliens'''
        #Create an alien and find the number of aliens in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        #calculates width of screen minus 2 aliens (1 alien on each side of screen)
        available_space_x = self.settings.screen_width - (2 * alien_width)
        #calculates how many aliens can fit (allows for one alien width beetween each alien)
            # // so we have an integer number of aliens
        number_aliens_x = available_space_x // (2 * alien_width)

        #calculate the number of rows of aliens that fit on the screen
        #have to leave room above ship for time to fire
        ship_height = self.ship.rect.height
        #calculates width of screen minus 2 aliens (1 alien on each side of screen)
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        #calculates how many aliens can fit (allows for one alien width beetween each alien)
            # // so we have an integer number of aliens
        number_rows = available_space_y // (2 * alien_height)


        #Create full fleet of aliens
        #outer loop counts from 0 to the number of rows we want
        for row_number in range(number_rows):
            #inner loop creates the aliens in one row
            for alien_number in range(number_aliens_x):
                #uses the alien number that is currently being created
                #uses row number so each row can be place farther down the screen 
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        '''Create an alien and place it in the row'''
        alien = Alien(self)
        #each alien is pushed to the right one alien width from the left margin
            #multiply alien width by 2 to account for the space each alien takes up, including the empty space to its right
            #multiply this amount by the alien's position in the row
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
            
        #set the postiion of its rect
        alien.rect.x = alien.x
        #each row starts two alien heights below the previous row
        alien.rect.y = alien_height + (2 * alien.rect.height * row_number)
        #add alien to group
        self.aliens.add(alien)

    
    def _check_fleet_edges(self):
        '''Respond appropriately if any aliens have reached an edge'''
        for alien in self.aliens.sprites():
            #if check_edges returns True, we know an alien is at the edge and the whole fleet must change directions
            if alien.check_edges():
                #if alien is at the edge, we call _change_fleet_direction() and break out of the loop
                self._change_fleet_direction()
                break

        
    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        #not part of the for loop because we want to change each alien's vertical position, but only want to change the direction of the fleet once
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        '''Respond to the ship being hit by an alien'''
        #Tests if player has at least one ship remaining 
        if self.stats.ships_left > 0:
            #Number of ships is reduced by 1
            self.stats.ships_left -= 1
            #update scoreboard
            self.sb.prep_ships()

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause so player can see ship has been hit
            sleep(0.5)
        
        #if player has no ships left, game will not be active, and mouse cursor will be visible again (so player can click play)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        '''Check if any aliens have reached the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break


    def _update_screen(self):
        #redraw the screen during each pass through the loop:
        self.screen.fill(self.settings.bg_color)

        #draw the ship on the screen
        self.ship.blitme()

        #sprites method returns a list of all sprites in the group bullet
            #to draw all fired bullets to screen, we loop through the sprites in bullets and call draw_bullet() on each one
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #draw alien
        self.aliens.draw(self.screen)

        #Draw the score information
        self.sb.show_score()

        #draw the play button if game is inactive
        #after all the other elements to make it visible above all other elements are drawn but before flipping to a new screen
        if not self.stats.game_active:
            self.play_button.draw_button()

        #make the most recently drawn screen visible:
            #draws an empty screen on each pass through the while loop
            #basically continually updates the display to create the illusion of smooth movement
        pygame.display.flip()


if __name__ == '__main__':
    #GAME INSTANCE:
    ai = AlienInvasion()
    ai.run_game()



'''
FINISHED BUT SCORES AREN'T UPDATING
CHECK PREP_SCORE??
'''