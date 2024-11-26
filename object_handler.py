from sprite_object import *
from npc import *
from pygame import mouse

class ObjectHandler():
    def __init__(self, game, npc_data = None, npc_sum = 0):
        self.game = game
        self.theme = game.theme
        self.sprite_list = []
        self._npc_list = npc_data
        self.npc_sprite_path = 'Resources/Sprites/NPC/'
        self.static_sprite_path = 'Resources/Sprites/Static_Sprites/'
        self.anim_sprite_path = 'Resources/Sprites/Animated_Sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self._npc_count = npc_sum

        self.static_Paths = ['Resources/Sprites/Static_Sprites/health-kit.png']
        self.animated_Paths = []

        if (self.npc_list == None):
            self.npc_list = []

            if (self.theme == "Halloween"):
                #self.static_Paths.append('Resources/Sprites/Static_Sprites/pumpkin.png')
                self.animated_Paths.append('Resources/Sprites/Animated_Sprites/Jack_Lantern/0.png')
                # spawn enemies
                add_npc(ZombieNPC(game, pos=(11.0, 19.0)))
                add_npc(ZombieNPC(game, pos=(11.5, 4.5)))
                add_npc(ZombieNPC(game, pos=(13.5, 6.5)))
                add_npc(ZombieNPC(game, pos=(2.0, 20.0)))
                add_npc(ZombieNPC(game, pos=(4.0, 29.0)))
                add_npc(ZombieNPC(game, pos=(5.5, 14.5)))
                add_npc(ZombieNPC(game, pos=(5.5, 16.5)))
                add_npc(ZombieNPC(game, pos=(14.5, 25.5)))
                self.npc_count = 8 #Make this equal num of npc spawned

            elif (self.theme == "Christmas"):
                #self.static_Paths.append('Resources/Sprites/Static_Sprites/pumpkin.png')
                #self.animated_Paths.append('Resources/Sprites/Animated_Sprites/Jack_Lantern/0.png')
                # spawn enemies
                add_npc(SlimeNPC(game, pos=(11.0, 19.0)))
                add_npc(SlimeNPC(game, pos=(11.5, 4.5)))
                add_npc(SlimeNPC(game, pos=(13.5, 6.5)))
                add_npc(SlimeNPC(game, pos=(2.0, 20.0)))
                add_npc(SlimeNPC(game, pos=(4.0, 29.0)))
                add_npc(SlimeNPC(game, pos=(5.5, 14.5)))
                add_npc(SlimeNPC(game, pos=(5.5, 16.5)))
                add_npc(SlimeNPC(game, pos=(14.5, 25.5)))
                self.npc_count = 8 #Make this equal num of npc spawned

            elif (self.theme == "Thanksgiving"):
                #self.static_Paths.append('Resources/Sprites/Static_Sprites/pumpkin.png')
                self.animated_Paths.append('Resources/Sprites/Animated_Sprites/Turkey/0.png')
                add_npc(TurkeyNPC(game, pos=(11.0, 19.0)))
                add_npc(TurkeyNPC(game, pos=(11.5, 4.5)))
                add_npc(TurkeyNPC(game, pos=(13.5, 6.5)))
                add_npc(TurkeyNPC(game, pos=(2.0, 20.0)))
                add_npc(TurkeyNPC(game, pos=(4.0, 29.0)))
                add_npc(TurkeyNPC(game, pos=(5.5, 14.5)))
                add_npc(TurkeyNPC(game, pos=(5.5, 16.5)))
                add_npc(TurkeyNPC(game, pos=(14.5, 25.5)))
                self.npc_count = 8 #Make this equal num of npc spawned


        self.npc_positions = {}

        # sprite map
        add_sprite(SpriteObject(game, self.static_Paths[0], health_value=10, scale=0.2, shift= 1))
        #add_sprite(AnimatedSprite(game, self.animated_Paths[0]))
 
    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

        if(self.npc_count == 0): #No more NPCs - player wins
            self.game.object_renderer.game_over()
            mouse.set_visible(True)
            self.game.sound.level_win.play()
            self.game.game.score_system.enter_new_score()
            mouse.set_visible(False)
            self.game.pause_menu.exit_to_menu() 

        if (self.npc_count <= 5 and self.theme == "Thanksgiving"):
            self.add_npc(TurkeyNPC(self.game, pos=(11.0, 19.0)))
            self.add_npc(TurkeyNPC(self.game, pos=(11.5, 4.5)))
            self.add_npc(TurkeyNPC(self.game, pos=(13.5, 6.5)))
            self.add_npc(TurkeyNPC(self.game, pos=(2.0, 20.0)))
            self.add_npc(TurkeyNPC(self.game, pos=(4.0, 29.0)))
            self.add_npc(TurkeyNPC(self.game, pos=(5.5, 14.5)))
            self.add_npc(TurkeyNPC(self.game, pos=(5.5, 16.5)))
            self.add_npc(TurkeyNPC(self.game, pos=(14.5, 25.5)))
            self.npc_count += 8

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    @property
    def npc_list(self):
        return self._npc_list
    
    @npc_list.setter
    def npc_list(self, value):
        self._npc_list = value

    @property
    def npc_count(self):
        return self._npc_count
    
    @npc_count.setter
    def npc_count(self, value):
        self._npc_count = value