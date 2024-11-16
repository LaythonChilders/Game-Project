from settings import *
import pygame as pygame
import math


class Player:
    def __init__ (self, catGame):
        self.catGame = catGame
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.catGame.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pygame.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collison(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.catGame.delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.catGame.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.catGame.map.world_map
    
    def check_wall_collison(self, dx, dy):
        # value used to maintain resolution of wall textures 
        SCALE = PLAYER_SIZE_SCALE / self.catGame.delta_time
        if self.check_wall(int(self.x + dx * SCALE), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * SCALE)):
            self.y += dy



    def draw(self):
        pygame.draw.line(self.catGame.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pygame.draw.circle(self.catGame.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.move()

    @property
    def pos(self):
        return self.x, self.y
    @property
    def map_pos(self):
        return int(self.x), int(self.y)