#class to store all settings for Alien Invasion:
class Settings:

    def __init__(self):
        #Initialize the game's settings
        #Screen Settings:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_speed = 5 #1.5
        self.ship_limit = 3

        #Bullet settings
            #bullets are set to 1.0 speed (slower than ship at 1.5)
        self.bullet_speed = 7.0 #1.5
        self.bullet_width = 3 
        self.bullet_height = 10 #15
        self.bullet_color = (60, 60, 60)
        #allows only 3 bullets at a time 
        self.bullets_allowed = 10 #3

        #Alien settings
        self.alien_speed = 4 #1.0
        #controls how quickly the fleet drops down the screen each tmie an alien reaches either edge
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1