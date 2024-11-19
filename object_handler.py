from sprite_object import *

class ObjectHandler():
    def __init__(self, game):
        self.game = game
        self.theme = game.theme
        self.sprite_list = []
        self.static_sprite_path = 'Resources/Sprites/Static_Sprites/'
        self.anim_sprite_path = 'Resources/Sprites/Animated_Sprites/'
        add_sprite = self.add_sprite

        self.static_Paths = []
        self.animated_Paths = []

        if (self.theme == "Halloween"):
            self.static_Paths.append('Resources/Sprites/Static_Sprites/pumpkin.png')
            self.animated_Paths.append('Resources/Sprites/Animated_Sprites/Jack_Lantern/0.png')

        elif (self.theme == "Christmas"):
            self.static_Paths.append('Resources/Sprites/Static_Sprites/pumpkin.png')
            self.animated_Paths.append('Resources/Sprites/Animated_Sprites/Jack_Lantern/0.png')

        elif (self.theme == "Thanksgiving"):
            self.static_Paths.append('Resources/Sprites/Static_Sprites/pumpkin.png')
            self.animated_Paths.append('Resources/Sprites/Animated_Sprites/Turkey/0.png')


        # sprite map
        add_sprite(SpriteObject(game, self.static_Paths[0]))
        add_sprite(AnimatedSprite(game, self.animated_Paths[0]))


    def update(self):
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)