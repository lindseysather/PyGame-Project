#class to store all settings for Alien Invasion:
class Settings:

    def __init__(self):
        #Initialize the game's settings
        #Screen Settings:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_speed = 1.5

        #Bullet settings
            #bullets are set to 1.0 speed (slower than ship at 1.5)
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        #allows only 3 bullets at a time 
        self.bullets_allowed = 3