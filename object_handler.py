from sprite_object import *

class ObjectHandler():
    def __init__(self, game):
        self.game = game
        self.theme = game.theme
        self.sprite_list = []
        self.static_sprite_path = 'Resources/Sprites/Static_Sprites/'
        self.anim_sprite_path = 'Resources/Sprites/Animated_Sprites/'
        add_sprite = self.add_sprite

        # sprite map
        if (self.theme == "Halloween"):
            add_sprite(SpriteObject(game, 'Resources/Sprites/Static_Sprites/pumpkin.png'))
            add_sprite(AnimatedSprite(game, 'Resources/Sprites/Animated_Sprites/Jack_Lantern/0.png'))
        
        elif (self.theme == "Christmas"):
            add_sprite(SpriteObject(game, 'Resources/Sprites/Static_Sprites/pumpkin.png'))
            add_sprite(AnimatedSprite(game, 'Resources/Sprites/Animated_Sprites/Jack_Lantern/0.png'))
        
        elif (self.theme == "Thanksgiving"):
            add_sprite(SpriteObject(game, 'Resources/Sprites/Static_Sprites/pumpkin.png'))
            add_sprite(AnimatedSprite(game, 'Resources/Sprites/Animated_Sprites/Turkey/0.png'))


    def update(self):
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)