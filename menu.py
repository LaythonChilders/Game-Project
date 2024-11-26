import pygame
import sys
from settings import *
from save_state import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.font = pygame.font.Font(None, 50)  # Default font with size 50
        self.running = True
        self.selected_theme = None  # Stores the selected theme as a string

        button_width = 700
        button_height = 50
        button_margin = 20

        self.buttons = [
            {
                "text": "Halloween Theme",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT - button_height - button_margin,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.set_theme("Halloween"),
            },
            {
                "text": "Christmas Theme",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.set_theme("Christmas"),
            },
            {
                "text": "Thanksgiving Theme - Endless",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT + button_height + button_margin,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.set_theme("Thanksgiving"),
            },
            {
                "text": "Load Game",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT + 2 * (button_height + button_margin) + button_margin,
                    button_width,
                    button_height,
                ),
                "action": self.load_game,
            },
        ]

    def set_theme(self, theme):
        self.game.theme = theme
        self.running = False
        self.game.init_theme_dependent()

    def draw_buttons(self):
        self.screen.fill('black')
        for button in self.buttons:
            pygame.draw.rect(self.screen, 'darkorange', button['rect'])
            text_surface = self.font.render(button["text"], True, 'white')
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            button["action"]()

    def load_game(self):
        self.game.state_saver.load_game_state()
        self.game.state_saver.apply_loaded_game_state()
        self.running = False

    def run(self):
        pygame.mouse.set_visible(True)
        while self.running:
            self.handle_events()
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.display.set_caption(f'{self.clock.get_fps(): .1f}')

        pygame.mouse.set_visible(False)

