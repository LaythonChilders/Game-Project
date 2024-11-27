import pygame
import sys
from settings import *
from save_state import *

class pause_menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.score_system = game.score_system
        self.font = pygame.font.Font(None, 50)  # Default font with size 50
        self.running = True
        self.initials = []

        button_width = 400
        button_height = 50
        num_buttons = 4  # Total number of buttons
        total_height = (button_height * num_buttons) + (20 * (num_buttons - 1))  # Buttons + gaps
        start_y = (HALF_HEIGHT - total_height // 2)  # Start vertically centered

        # Create buttons dynamically with even spacing
        self.buttons = []
        button_texts = ["Return to main menu", "Restart level", "Save Game", "Exit"]
        button_actions = [self.exit_to_menu, self.restart_level, self.save_game, self.exit_game]

        for i in range(num_buttons):
            y_position = start_y + i * (button_height + 20)  # Calculate y-position dynamically
            self.buttons.append({
                "text": button_texts[i],
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    y_position,
                    button_width,
                    button_height,
                ),
                "action": button_actions[i],
            })

    def restart_level(self):
        self.game.running = False
        self.running = False
        self.game.restart_level()

    def exit_to_menu(self):
        self.game.running = False
        self.running = False
        self.game.setup_game()

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def save_game(self):
        state_saver = save_state(self.game)
        state_saver.get_game_state()
        state_saver.save_game_state()

        self.game.running = False
        self.running = False
        self.game.setup_game()

    def draw_nav_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, 'darkorange', button['rect'])
            text_surface = self.font.render(button["text"], True, 'white')
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            button["action"]()

    def run(self):
        self.running = True

        while self.running:
            self.game.object_renderer.draw_top_scores()
            self.draw_nav_buttons()
            
            self.handle_events()

            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')
