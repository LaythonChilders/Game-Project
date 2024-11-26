import pygame as pygame
import sys
from settings import *
from map import * 
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from menu import *
from pause_menu import *
from weapon import *
from sound import *
from pathfinding import *
from score_system import *

# Factories and singleton TO IMPLEMENT
class CatDoom:
    def __init__(self):
        pygame.init()
        pygame.event.set_grab(True)
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 40)
        self.state_saver = save_state(self)

    def new_game(self):
        self.map = Map(self)
        self.score_system = Score_system(self)
        self.player = Player(self)
        self.menu = Menu(self)
        self.pause_menu = pause_menu(self)
        self.weapon = Weapon(self)
        self.pathfinding = PathFinding(self)
        self.running = True

    def init_theme_dependent(self):
        self.object_handler = ObjectHandler(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = Raycasting(self)
        self.sound = Sound(self)

    def load_save_theme_dependent(self, npc_list, npc_amt):
        self.object_handler = ObjectHandler(self, npc_list, npc_sum = npc_amt)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = Raycasting(self)
        self.sound = Sound(self)

    def draw_frame(self): #called in loop to update/redraw each frame
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Check for user intent to exit outside of pause menu
                pygame.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True

            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): #if user presses escape show pause menu
                pygame.mouse.set_visible(True)
                self.pause_menu.run()
                pygame.mouse.set_visible(False)

            self.player.single_fire_event(event)

    def check_exit(self): # checks for events/keystrokes that signal user intent to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def main_loop(self):
        while self.running:
            self.check_exit()
            self.draw_frame()
            self.draw()
            self.check_events()
            
    def setup_game(self):
        self.new_game()
        self.menu.run()


    def restart_level(self):
        pygame.mouse.set_visible(False)
        self.new_game()
        self.init_theme_dependent()
        self.main_loop()


if __name__ == '__main__':
    catGame = CatDoom()
    catGame.setup_game()
    catGame.main_loop()

