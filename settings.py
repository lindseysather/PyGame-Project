#class to store all settings for Alien Invasion:
class Settings:

    def __init__(self):
        #Initialize the game's STATIC settings (doens't include speed that changes each level)
        #Screen Settings:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 3 
        self.bullet_height = 10 #15
        self.bullet_color = (60, 60, 60)
        #allows only 3 bullets at a time 
        self.bullets_allowed = 10 #3

        #Alien settings
        #controls how quickly the fleet drops down the screen each tmie an alien reaches either edge
        self.fleet_drop_speed = 10 #10

        #How quickly the game speeds up
        self.speedup_scale = 3#1.1

        #How quickly the alien point values increase
        self.score_scale = 1.5
        
        #initialize values for attributes that need to change throughout the game
        self.initialize_dynamic_settings()
        

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 5.0 #1.0

        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        #Scoring - gets 50 points every time you shoot down an alien
        self.alien_points = 50


    def increase_speed(self):
        '''Increase speed settings and alien point values'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        #print(self.alien_points)