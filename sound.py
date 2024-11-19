import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'Resources/Sounds/'
        self.minigun = pg.mixer.Sound(self.path + 'bottle-pop.mp3')
        self.reload = pg.mixer.Sound(self.path + 'gun-reload.mp3')
