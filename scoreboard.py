#import this because Scoreboard writes text to the screen 
import pygame.font

class Scoreboard:
    '''A class to report scoring information.'''

    #give ai_game parameter so it can access settings, screen, and stats objects
    def __init__(self, ai_game):
        '''Initialize scorekeeping attributes'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #prepare the initial score image
        self.prep_score()

    def prep_score(self):
        '''Turn the score into a rendered image'''
        #turn numerical score value into string so we can pass it to render() to make it an image
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #Display score at the top right of screen (expands to the left as score increases and the width of the number grows)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        '''Draw score to the screen'''
        self.screen.blit(self.score_image, self.score_rect)