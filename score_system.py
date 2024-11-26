import json
from settings import *
import pygame
import sys
import string

class Score_system:
    def __init__(self, game, filename="scores.json"):
        self._current_score = 0
        self.filename = filename
        self.game = game
        self.clock = game.clock
        self._top_scores = self.load_top_scores()
        self.initials = []

    def save_top_scores(self):
        """Save the top 10 top_scores to a JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.top_scores, file, indent=4)

    def load_top_scores(self):
            try:
                with open(self.filename, "r") as file:
                    return json.load(file)
            except FileNotFoundError:
                # Create the file with an empty list
                with open(self.filename, "w") as file:
                    json.dump([], file, indent=4)
                return []

    def write_new_score(self, initials, score):
        self.top_scores.append({"initials": initials, "score": score})
        
        self.top_scores.sort(key=lambda x: x["score"], reverse=True)
        
        self.top_scores = self.top_scores[:10]
        
        self.save_top_scores()

    def add_points(self, value):
        self.current_score += value
    
    def handle_events(self):
        button_size = 50
        spacing = 10
        start_x = (WIDTH - (button_size + spacing) * 13) // 2
        start_y = HEIGHT - 180
        enter_x = WIDTH // 2 - button_size
        enter_y = start_y + 2 * (button_size + spacing)
        max_initials = 3

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # Handle letter buttons
                for i, char in enumerate(string.ascii_uppercase):
                    col = i % 13
                    row = i // 13
                    x = start_x + col * (button_size + spacing)
                    y = start_y + row * (button_size + spacing)
                    rect = pygame.Rect(x, y, button_size, button_size)
                    if rect.collidepoint(mouse_pos) and len(self.initials) < max_initials:
                        self.initials.append(char)
                        break

                # Handle "Enter" button
                enter_rect = pygame.Rect(enter_x, enter_y, button_size * 2, button_size)
                if enter_rect.collidepoint(mouse_pos) and len(self.initials) == max_initials:
                    self.write_new_score("".join(self.initials), self.current_score)
                    self.save_top_scores()
                    self.running = False

                # Handle "Skip" button
                skip_x = WIDTH // 2 - button_size * 4
                skip_rect = pygame.Rect(skip_x, enter_y, button_size * 2, button_size)
                if skip_rect.collidepoint(mouse_pos):
                    self.running = False  # Exit without saving initials

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def enter_new_score(self):
        self.running = True

        while (self.running):
            self.game.object_renderer.draw_score_system_enter_data(self.initials)

            self.handle_events()

            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')




    @property
    def top_scores(self):
        return self._top_scores
    
    @top_scores.setter
    def top_scores(self, value):
        self._top_scores = value

    @property
    def current_score(self):
        return self._current_score
    
    @current_score.setter
    def current_score(self, value):
        self._current_score = value