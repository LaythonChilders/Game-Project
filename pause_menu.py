import pygame
import sys
from settings import *

class pause_menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.font = pygame.font.Font(None, 50)  # Default font with size 50
        self.running = True

        button_width = 400
        button_height = 50
        button_margin = 20

        self.buttons = [
            {
                "text": "Return to main menu",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT - button_height - button_margin,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.exit_game(),
            },
            {
                "text": "Exit",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.exit_game(),
            },
        ]

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, 'darkorange', button['rect'])
            text_surface = self.font.render(button["text"], True, 'white')
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
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
            self.clock.tick(FPS)
            pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')