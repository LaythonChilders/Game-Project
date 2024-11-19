from sprite_object import *

class Weapon(AnimatedSprite):
    def _init__(self, game, path='resources/sprites/weapon/shotgun/wiedlingMinigun.png', scale=0.4, animation_time=90):
        super()._init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_ppos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.image[0].get_height())

        def draw(self):
            self.game.screen.blit(self.images[0], self.weapon_pos)

        def update(self):
            pass