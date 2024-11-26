from sprite_object import *
from random import randint, random, choice

class NPCFactory:
    
    #Factory for creating NPCs.
    @staticmethod
    def create_npc(npc_type, game, pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        if npc_type == "zombie":
            return ZombieNPC(game, pos=pos, scale=scale, shift=shift, animation_time=animation_time)
        elif npc_type == "turkey":
            return TurkeyNPC(game, pos=pos, scale=scale, shift=shift, animation_time=animation_time)
        elif npc_type == "slime":
            return SlimeNPC(game, pos=pos, scale=scale, shift=shift, animation_time=animation_time)
        else:
            raise ValueError(f"Unknown NPC type: {npc_type}")

class NPC(AnimatedSprite):
    def __init__(self, game, path, pos=(10.5, 5.5),
                 scale=0.6, shift=0.3, animation_time=180, point_value=10, health_value = 0, attack_damage=10, health = 100):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/Attack')
        self.death_images = self.get_images(self.path + '/Death')
        self.idle_images = self.get_images(self.path + '/Idle')
        self.pain_images = self.get_images(self.path + '/Pain')
        self.walk_images = self.get_images(self.path + '/Walk')

        self.attack_dist = randint(1, 1)
        self.speed = 0.03
        self.size = 10
        self._health = health
        self.attack_damage = attack_damage
        self.accuracy = 0.90
        self.alive = True if self.health > 1 else False
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.point_value = point_value
        self.health_granted = False
        self.health_value = health_value

        self.scale = scale
        self.shift = shift

    def grant_health_to_player(self):
        if not self.alive and not self.health_granted and self.player.health < 100 and self.health_value != 0:
            if self.dist < 1.0: 
                self.game.player.add_health(self.health_value)
                self.health_granted = True              

    def update(self):
        self.check_animation_time()
        if(self.health_granted == False):
            self.get_sprite()
        self.run_logic()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        # value used to maintain resolution of wall textures 
        SCALE = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:
                pass
                self.game.player.take_damage(self.attack_damage)

    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_shot.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()
            self.game.score_system.add_points(self.point_value)
            self.game.object_handler.npc_count = self.game.object_handler.npc_count - 1

    def run_logic(self):
        if self.alive == True:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True 

                if self.dist < self.attack_dist:
                    self.animate(self.images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()
            self.grant_health_to_player()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True
        
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1,1
        
        if self.theta == 0:
            dx = self.x - self.player.x
            dy = self.y - self.player.y
            self.dx, self.dy = dx, dy
            self.theta = math.atan2(dy, dx)

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        
        #horizontal
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a
        
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        #vertical
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)

class ZombieNPC(NPC):
    def __init__(self, game, path='Resources/Sprites/NPC/Zombie/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

class TurkeyNPC(NPC):
    def __init__(self, game, path='Resources/Sprites/NPC/Turkey/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time, health_value=2)

class SlimeNPC(NPC):
    def __init__(self, game, path='Resources/Sprites/NPC/Slime/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.3, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time, attack_damage=20)