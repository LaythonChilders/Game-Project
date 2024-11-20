from settings import *
import pygame as pygame
import math
from scoreboard import *


class Player:
    def __init__ (self, catGame):
        self.catGame = catGame
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.score = 0
        self.scoreboard = Scoreboard(self)

    def check_game_over(self):
        if self.health < 1:
            self.catGame.object_renderer.game_over()
            pygame.display.flip()
            pygame.time.delay(1500)
            
            self.scoreboard.add_score("LTC", self.score)
            print(self.scoreboard.get_scores())
            
            self.catGame.restart_level()



    def get_damage(self, damage):
        self.health -= damage
        self.catGame.object_renderer.player_damage()
        self.catGame.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
                        
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.catGame.weapon.reloading:
                self.catGame.sound.shotgun.play()
                self.catGame.sound.reload.play()
                self.shot = True
                self.catGame.weapon.reloading = True

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

    #    if keys[pygame.K_LEFT]:
    #        self.angle -= PLAYER_ROT_SPEED * self.catGame.delta_time
    #    if keys[pygame.K_RIGHT]:
    #        self.angle += PLAYER_ROT_SPEED * self.catGame.delta_time
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

    def mouse_control(self):
        mx, my = pygame.mouse.get_pos()
        #if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
        pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.catGame.delta_time

    def update(self):
        self.move()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y
    @property
    def map_pos(self):
        return int(self.x), int(self.y)