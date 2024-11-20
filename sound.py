import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'Resources/Sounds/'
        self.shotgun = pg.mixer.Sound(self.path + 'bottle-pop.mp3')
        self.reload = pg.mixer.Sound(self.path + 'gun-reload.mp3')
        self.npc_shot = pg.mixer.Sound(self.path + 'zombie-bite.mp3')
        self.npc_death = pg.mixer.Sound(self.path + 'zombie-death.mp3')
        self.player_pain = pg.mixer.Sound(self.path + 'player-death.mp3')

