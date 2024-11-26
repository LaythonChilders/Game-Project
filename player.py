from settings import *
import pygame as pygame
import math

class Player:
    def __init__ (self, catGame, map_pos = PLAYER_POS, health = PLAYER_MAX_HEALTH, angle = PLAYER_ANGLE):
        self._catgame = catGame
        self._x, self._y = map_pos
        self._angle = angle
        self._shot = False
        self._health = health

    def check_game_over(self):
        if self._health < 1:
            self._catgame.object_renderer.game_over()
            pygame.display.flip()
            pygame.time.delay(1500)
            
            pygame.mouse.set_visible(True)
            self._catgame.score_system.enter_new_score()
            pygame.mouse.set_visible(False)
            
            self._catgame.restart_level()

    def take_damage(self, damage):
        self._health -= damage
        self._catgame.object_renderer.player_damage()
        self._catgame.sound.player_pain.play()
        self.check_game_over()

    def add_health(self, health_value):
        if self._health < PLAYER_MAX_HEALTH:
            self._health = min(self._health + health_value, PLAYER_MAX_HEALTH)
            self._catgame.sound.health_pickup.play()

    def single_fire_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self._shot and not self._catgame.weapon.reloading:
                self._catgame.sound.shotgun.play()
                self._catgame.sound.reload.play()
                self._shot = True
                self._catgame.weapon.reloading = True

    def move(self):
        sin_a = math.sin(self._angle)
        cos_a = math.cos(self._angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self._catgame.delta_time
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
    #        self._angle -= PLAYER_ROT_SPEED * self._catgame.delta_time
    #    if keys[pygame.K_RIGHT]:
    #        self._angle += PLAYER_ROT_SPEED * self._catgame.delta_time
        self._angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self._catgame.map.world_map
    
    def check_wall_collison(self, dx, dy):
        # value used to maintain resolution of wall textures 
        SCALE = PLAYER_SIZE_SCALE / self._catgame.delta_time
        if self.check_wall(int(self._x + dx * SCALE), int(self._y)):
            self._x += dx
        if self.check_wall(int(self._x), int(self._y + dy * SCALE)):
            self._y += dy

    def draw(self):
        pygame.draw.line(self._catgame.screen, 'yellow', (self._x * 100, self._y * 100),
                    (self._x * 100 + WIDTH * math.cos(self._angle),
                     self._y * 100 + WIDTH * math. sin(self._angle)), 2)
        pygame.draw.circle(self._catgame.screen, 'green', (self._x * 100, self._y * 100), 15)

    def mouse_control(self):
        mx, my = pygame.mouse.get_pos()
        #if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
        pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self._angle += self.rel * MOUSE_SENSITIVITY * self._catgame.delta_time

    def update(self):
        self.move()
        self.mouse_control()

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def pos(self):
        return self._x, self._y
    
    @property
    def map_pos(self):
        return int(self._x), int(self._y)
    
    @map_pos.setter
    def map_pos(self, value):
        self._x = value[0]
        self._y = value[1]

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
    
    @property
    def shot(self):
        return self._shot
    
    @shot.setter
    def shot(self, value):
        self._shot = value