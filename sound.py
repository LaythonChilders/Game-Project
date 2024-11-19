import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'Resources/Sounds/'
        self.shotgun = pg.mixer.Sound(self.path + 'bottle-pop.mp3')
        self.reload = pg.mixer.Sound(self.path + 'gun-reload.mp3')
        self.npc_shot = pg.mixer.Sound(self.path + 'bleah1.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'bleah1.wav')

