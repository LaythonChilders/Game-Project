import pygame as pygame
import sys
from settings import *
from map import * 
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *


class CatDoom:
    def __init__(self):
        pygame.init()
        # not working????
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game() 

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = Raycasting(self)
        #self.static_sprite = SpriteObject(self)
        #self.animated_sprite = AnimatedSprite(self)
        self.object_handler = ObjectHandler(self)

    def draw_frame(self): #called in loop to update/redraw each frame
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        #self.static_sprite.update()
        #self.animated_sprite.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def draw(self):
       # self.screen.fill('black')
        self.object_renderer.draw()
        #self.map.draw()
        #self.player.draw()


    def check_exit(self): # checks for events/keystrokes that signal user intent to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def main_loop(self):
        while True:
            self.check_exit()
            self.draw_frame()
            self.draw()

if __name__ == '__main__':
    catGame = CatDoom()
    catGame.main_loop() 