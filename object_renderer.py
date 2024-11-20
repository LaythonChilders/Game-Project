import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.theme = game.theme
        self.wall_textures = self.load_wall_textures()
        if (self.theme == "Thanksgiving"):
            self.sky_image = self.get_texture('Resources/Textures/sky.png', (WIDTH, HALF_HEIGHT))
        elif (self.theme == "Halloween"):
            self.sky_image = self.get_texture('Resources/Textures/halloweenSky.png', (WIDTH, HALF_HEIGHT))
        elif (self.theme == "Christmas"):
            self.sky_image = self.get_texture('Resources/Textures/christmasSky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('Resources/Textures/blood_screen.png', RESOLUTION)
        self.digit_size= 90
        self.digit_images = [self.get_texture(f'Resources/Textures/Digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('Resources/Textures/game_over.png', RESOLUTION)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0,0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i +1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # Floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        if (self.theme == "Halloween"):
            return {
                1: self.get_texture('Resources/Textures/stoneWall.png'),
                2: self.get_texture('Resources/Textures/stoneWall.png'),
                3: self.get_texture('Resources/Textures/stoneWall.png'),
                4: self.get_texture('Resources/Textures/stoneWall.png'),
                5: self.get_texture('Resources/Textures/stoneWall.png'),
            }
        elif (self.theme == "Christmas"):
            return {
                1: self.get_texture('Resources/Textures/christmaswall.png'),
                2: self.get_texture('Resources/Textures/christmaswall.png'),
                3: self.get_texture('Resources/Textures/christmaswall.png'),
                4: self.get_texture('Resources/Textures/christmaswall.png'),
                5: self.get_texture('Resources/Textures/christmaswall.png'),
            }
        elif (self.theme == "Thanksgiving"):
            return {
                1: self.get_texture('Resources/Textures/thanksgivingwall.png'),
                2: self.get_texture('Resources/Textures/thanksgivingwall.png'),
                3: self.get_texture('Resources/Textures/thanksgivingwall.png'),
                4: self.get_texture('Resources/Textures/thanksgivingwall.png'),
                5: self.get_texture('Resources/Textures/thanksgivingwall.png'),
            }
            