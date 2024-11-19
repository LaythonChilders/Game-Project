import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'Resources/Sounds/'
        self.shotgun = pg.mixer.Sound(self.path + 'bleah1.ogg')
