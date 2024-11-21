import string
import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.theme = game.theme
        self.player = game.player
        self.wall_textures = self.load_wall_textures()
        if (self.theme == "Thanksgiving"):
            self.sky_image = self.get_texture('Resources/Textures/sky.png', (WIDTH, HALF_HEIGHT))
        elif (self.theme == "Halloween"):
            self.sky_image = self.get_texture('Resources/Textures/stormySky.png', (WIDTH, HALF_HEIGHT))
        elif (self.theme == "Christmas"):
            self.sky_image = self.get_texture('Resources/Textures/nightSky2.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('Resources/Textures/blood_screen.png', RESOLUTION)
        self.game_over_image = self.get_texture('Resources/Textures/catOver.png', RESOLUTION)
        
        self.digit_size= 90
        self.digit_images = [self.get_texture(f'Resources/Textures/Digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        
        self.letter_size= 120
        self.letter_images = [self.get_texture(f'Resources/Textures/Letters/{char}.png', [self.letter_size] * 2)
                      for char in string.ascii_uppercase]
        self.letter_images.append(self.get_texture(f'Resources/Textures/Letters/colon.png', [self.letter_size] * 2))
        keys = list(string.ascii_uppercase) + [":"]  # A-Z + :
        self.letters = dict(zip(keys, self.letter_images))
        
        ##dict for scoreboard
        self.scoreboard_digit_size= 35
        self.scoreboard_digit_images = [self.get_texture(f'Resources/Textures/Digits/{i}.png', [self.scoreboard_digit_size] * 2)
                             for i in range(11)]
        self.scoreboard_digits = dict(zip(map(str, range(11)), self.scoreboard_digit_images))
        
        self.scoreboard_letter_size= 35
        self.scoreboard_letter_images = [self.get_texture(f'Resources/Textures/Letters/{char}.png', [self.scoreboard_letter_size] * 2)
                      for char in string.ascii_uppercase]
        self.scoreboard_letter_images.append(self.get_texture(f'Resources/Textures/Letters/colon.png', [self.scoreboard_letter_size] * 2))
        keys = list(string.ascii_uppercase) + [":"]  # A-Z + :
        self.scoreboard_letters = dict(zip(keys, self.scoreboard_letter_images))

        self.character_health_images = self.load_character_health_images()

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_player_score()
        #self.draw_scoreboard()
        self.show_character_health()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0,0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i +1) * self.digit_size, 0))

    def show_character_health(self):
        """Displays the character image based on the player's current health."""
        health = self.player.health
        if health > 75:
            image = self.character_health_images[100]
        elif health > 50:
            image = self.character_health_images[75]
        elif health > 25:
            image = self.character_health_images[50]
        elif health > 10:
            image = self.character_health_images[25]
        else:
            image = self.character_health_images[10]

        image_rect = image.get_rect(bottomright=(WIDTH, HEIGHT))
        self.screen.blit(image, image_rect)

    def load_character_health_images(self):
        health_images = {
            100: self.get_texture('Resources/character/character100.png'),
            75: self.get_texture('Resources/character/character75.png'),
            50: self.get_texture('Resources/character/character50.png'),
            25: self.get_texture('Resources/character/character25.png'),
            10: self.get_texture('Resources/character/character10.png'),
        }
        return health_images

    def draw_player_score(self):
        score = str(self.game.player.score)
        text_width = self.letter_size * 6
        total_score_width = text_width + len(score) * self.digit_size
        start_x = WIDTH - total_score_width

        
        self.screen.blit(self.letters['S'], (start_x + 0 * self.letter_size, 0))  # S
        self.screen.blit(self.letters['C'],  (start_x + 1 * self.letter_size, 0))  # C
        self.screen.blit(self.letters['O'], (start_x + 2 * self.letter_size, 0))  # O
        self.screen.blit(self.letters['R'], (start_x + 3 * self.letter_size, 0))  # R
        self.screen.blit(self.letters['E'],  (start_x + 4 * self.letter_size, 0))  # E
        self.screen.blit(self.letters[':'], (start_x + 5 * self.letter_size, 0))  # :

        digit_start_x = start_x + text_width  
        for i, char in enumerate(score):
            self.screen.blit(self.digits[char], (digit_start_x + i * self.digit_size, 0))


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
                4: self.get_texture('Resources/Textures/brick.png'),
                5: self.get_texture('Resources/Textures/metal.png'),
            }
        elif (self.theme == "Christmas"):
            return {
                1: self.get_texture('Resources/Textures/christmaswall.png'),
                2: self.get_texture('Resources/Textures/christmaswall.png'),
                3: self.get_texture('Resources/Textures/christmaswall.png'),
                4: self.get_texture('Resources/Textures/brick2.png'),
                5: self.get_texture('Resources/Textures/christmasTree.png'),
            }
        elif (self.theme == "Thanksgiving"):
            return {
                1: self.get_texture('Resources/Textures/thanksgivingwall.png'),
                2: self.get_texture('Resources/Textures/thanksgivingwall.png'),
                3: self.get_texture('Resources/Textures/thanksgivingwall.png'),
                4: self.get_texture('Resources/Textures/brick2.png'),
                5: self.get_texture('Resources/Textures/thanksgivingwall.png'),
            }
    
    def draw_scoreboard(self):
        scores = self.player.scoreboard.get_scores()

        start_x = HALF_WIDTH - 500 
        start_y = HEIGHT // 3 * 2
        row_height = self.scoreboard_letter_size + 20  #
        column_offset = WIDTH // 2
        
        for index, score_entry in enumerate(scores):
            column = index // 5  
            row = index % 5  

            
            x = start_x + column * column_offset
            y = start_y + row * row_height

            if index == 9:
                x -= self.scoreboard_digit_size 
           
            rank = str(index + 1)
            for i, char in enumerate(rank):
                self.screen.blit(self.scoreboard_digits[char], (x + i * self.scoreboard_digit_size, y))

            
            initials_x = x + len(rank) * self.scoreboard_digit_size + self.scoreboard_letter_size
            for i, char in enumerate(score_entry["initials"]):
                self.screen.blit(self.scoreboard_letters[char.upper()], (initials_x + i * self.scoreboard_letter_size, y))

            
            score_str = str(score_entry["score"])
            score_x = initials_x + len(score_entry["initials"]) * self.scoreboard_letter_size + self.scoreboard_letter_size
            for i, char in enumerate(score_str):
                self.screen.blit(self.scoreboard_digits[char], (score_x + i * self.scoreboard_digit_size, y))

    def draw_scoreboard_enter_data(self, initials="ZZZ", highlight_index=None):
        max_initials = 3
        button_size = 50
        spacing = 10
        start_x = (WIDTH - (button_size + spacing) * 13) // 2
        start_y = HEIGHT - 180

        initials_area_height = button_size + spacing + 10  
        initials_area_rect = pg.Rect(0, start_y - initials_area_height, WIDTH, initials_area_height)
        pg.draw.rect(self.screen, (0, 0, 0), initials_area_rect)

        
        for i, char in enumerate(string.ascii_uppercase):
            col = i % 13
            row = i // 13
            x = start_x + col * (button_size + spacing)
            y = start_y + row * (button_size + spacing)

            color = (255, 255, 255) 
            if highlight_index is not None and i == highlight_index:
                color = (255, 0, 0) 

            pg.draw.rect(self.screen, color, (x, y, button_size, button_size), border_radius=5)

            letter_image = self.get_texture(f'Resources/Textures/Letters/{char}.png', (button_size, button_size))
            self.screen.blit(letter_image, (x, y))

        initials_x = WIDTH // 2 - (button_size + spacing) * len(initials) // 2
        initials_y = start_y - button_size - spacing
        for i, char in enumerate(initials):
            letter_image = self.get_texture(f'Resources/Textures/Letters/{char}.png', (button_size, button_size))
            self.screen.blit(letter_image, (initials_x + i * (button_size + spacing), initials_y))

        enter_x = WIDTH // 2 - button_size
        enter_y = start_y + 2 * (button_size + spacing)
        button_color = (0, 255, 0) if len(initials) == max_initials else (100, 100, 100)
        pg.draw.rect(self.screen, button_color, (enter_x, enter_y, button_size * 2, button_size), border_radius=5)

        font = pg.font.Font(None, 36)
        enter_text = font.render("Enter", True, (0, 0, 0))
        self.screen.blit(enter_text, (enter_x + 15, enter_y + 10))
