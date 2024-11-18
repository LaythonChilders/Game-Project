import pygame
import sys
from settings import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.font = pygame.font.Font(None, 50)  # Default font with size 50
        self.running = True
        self.selected_theme = None  # Stores the selected theme as a string

        button_width = 400
        button_height = 50
        button_margin = 20

        self.buttons = [
            {
                "text": "Halloween Theme",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT - button_height - button_margin // 2,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.set_theme("Halloween"),
            },
            {
                "text": "Christmas Theme",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT + button_margin // 2,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.set_theme("Christmas"),
            },
        ]

    def set_theme(self, theme):
        self.selected_theme = theme
        self.running = False

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

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(60)
        return self.selected_theme
