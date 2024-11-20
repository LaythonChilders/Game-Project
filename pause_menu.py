import pygame
import sys
from settings import *
import string

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
                "action": lambda: self.exit_to_menu(),
            },
            {
                "text": "Restart level",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.restart_level(),
            },
            {
                "text": "Exit",
                "rect": pygame.Rect(
                    HALF_WIDTH - button_width // 2,
                    HALF_HEIGHT + button_height + button_margin,
                    button_width,
                    button_height,
                ),
                "action": lambda: self.exit_game(),
            },
        ]
    
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

    def handle_death_events(self, initials, max_initials):
        """
        Handles events for the death screen, allowing the user to input initials.
        """
        button_size = 50
        spacing = 10
        start_x = (WIDTH - (button_size + spacing) * 13) // 2
        start_y = HEIGHT - 150
        enter_x = WIDTH // 2 - button_size
        enter_y = start_y + 2 * (button_size + spacing)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_pos = event.pos

                # Check if a letter button is clicked
                for i, char in enumerate(string.ascii_uppercase):
                    col = i % 13
                    row = i // 13
                    x = start_x + col * (button_size + spacing)
                    y = start_y + row * (button_size + spacing)
                    rect = pygame.Rect(x, y, button_size, button_size)
                    if rect.collidepoint(mouse_pos) and len(initials) < max_initials:
                        initials.append(char)
                        break

                # Check if the "Enter" button is clicked
                enter_rect = pygame.Rect(enter_x, enter_y, button_size * 2, button_size)
                if enter_rect.collidepoint(mouse_pos) and len(initials) == max_initials:
                    self.game.player.scoreboard.add_score("".join(initials), self.game.player.score)
                    self.game.player.scoreboard.save_scores()
                    self.running = False  # Exit the death screen loop

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while self.running:
            self.game.object_renderer.draw_scoreboard()
            self.handle_events()
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def death(self):
        initials = []
        max_initials = 3

        while self.running:
            self.handle_death_events(initials, max_initials)  # Call event handler
            self.game.object_renderer.draw_scoreboard_enter_data(initials)
            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')