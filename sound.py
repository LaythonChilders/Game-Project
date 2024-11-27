import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game

        if pg.mixer.get_init():
            pg.mixer.quit()

        pg.mixer.init()

        self.path = 'Resources/Sounds/'
        self.shotgun = pg.mixer.Sound(self.path + 'bottle-pop.mp3')
        self.reload = pg.mixer.Sound(self.path + 'gun-reload.mp3')
        self.player_pain = pg.mixer.Sound(self.path + 'player-death.mp3')
        self.health_pickup = pg.mixer.Sound(self.path + 'health-pickup.mp3')
        self.level_win = pg.mixer.Sound(self.path + 'level-win.mp3')
        self.menu_music = pg.mixer.Sound(self.path + 'MenuMusic.mp3')


    def init_theme_sounds(self, theme):

        if (theme == "Thanksgiving"):
            self.npc_death = pg.mixer.Sound(self.path + 'turkey-death.mp3')
            self.npc_shot = pg.mixer.Sound(self.path + 'turkey-pain.mp3')

        elif (theme == "Halloween"):
            self.npc_death = pg.mixer.Sound(self.path + 'zombie-death.mp3')
            self.npc_shot = pg.mixer.Sound(self.path + 'zombie-bite.mp3')

        elif (theme == "Christmas"):
            self.npc_death = pg.mixer.Sound(self.path + 'slime-death.mp3')
            self.npc_shot = pg.mixer.Sound(self.path + 'slime-hurt.mp3')
