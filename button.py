import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        '''Initialize button attributions.'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        #non is the default font:
        self.font = pygame.font.SysFont(None, 48)

        #build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #the button message needs to be prepped only once
        self._prep_msg(msg)


    def _prep_msg(self, msg):
        '''Turn msg into a rendered image and center text on the button'''
        #font.render() turns text in msg into an image (stored in self.msg_image) 
            #also takes a Boolean value to turn antialiasing onn or off (make edges of text smoother)
            #also gets font color and background color - set text background color to the same color as the button
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        #create rect:
        self.msg_image_rect = self.msg_image.get_rect()
        #center rect:
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''Draw blank buttonn and then draw message'''
        #draw rectangle portion of button:
        self.screen.fill(self.button_color, self.rect)
        #draw the text image to the screen 
        self.screen.blit(self.msg_image, self.msg_image_rect)