#import this because Scoreboard writes text to the screen 
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    '''A class to report scoring information.'''

    #give ai_game parameter so it can access settings, screen, and stats objects
    def __init__(self, ai_game):
        '''Initialize scorekeeping attributes'''
        #assign game instance to attributee
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        '''Turn the score into a rendered image'''
        #-1 rounds the value to the nearest 10, 100, 1000, etc. (rounds value of stats.score to the nearest 10 and stores it in rounded_score)
        rounded_score = round(self.stats.score, -1)
        #format tells to insert commas into numbers when converting a numerical value to a string
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #Display score at the top right of screen (expands to the left as score increases and the width of the number grows)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def show_score(self):
        '''Draw scores, level, and ships to the screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #display ships on the screen 
        self.ships.draw(self.screen)


    def prep_high_score(self):
        '''Turn the high score into a rendered image.'''
        #round to the nearest 10 and format with commas
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        #generate an image from the high score
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        #Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        #center horizontally 
        self.high_score_rect.centerx = self.screen_rect.centerx
        #set rect's top attribute to match the top of the score image 
        self.high_score_rect.top = self.score_rect.top


    def check_high_score(self):
        '''Check to see if there's a new high score'''
        #if the current score is greater, we upadte the value of high_score and call prep_high_score() to update the high score's image
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    #creates an image from the value stored in stats.level
    def prep_level(self):
        '''Turn the level into a rendered image'''
        level_str = str(self.stats.level)
        #sets image's right attribute to match the score's right attribute
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        #Position the level below the score
            #sets the top attribute 10 pixels beneath the bottom of the score image to leave space between the score and the level
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    
    def prep_ships(self):
        '''Show how many ships are left'''
        #create an empty group to hold ship instances
        self.ships = Group()
        #to fill the group, loop runs once for every ship the player has left
        for ship_number in range(self.stats.ships_left):
            #create a new ship 
            ship = Ship(self.ai_game)
            #set each ship's x-coordinate value so the ships appear next to each other with a 10 pixel margin on the left side of the group of ships
            ship.rect.x = 10 + ship_number * ship.rect.width
            #set y-coordinate value 10 pixels down from the top of the screen
            ship.rect.y = 10
            #add each new ship to the group ships
            self.ships.add(ship)

 