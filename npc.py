from sprite_object import *
from random import randint, random, choice

class NPC(AnimatedSprite):
    def __init__(self, game, path='Resources/Sprites/NPC/Turkey/0.png', pos=(10.5, 5.5),
                scale=0.6, shift=0.3, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
    