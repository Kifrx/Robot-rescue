import pygame
from settings import *

# BUTTON CLASS
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    # DRAW BUTTON
    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Shadow
        shadow_rect = self.rect.move(3, 3)
        pygame.draw.rect(screen, (100, 100, 100), shadow_rect, border_radius=10)

        # Warna utama
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Border
        pygame.draw.rect(screen, (40, 40, 40), self.rect, 2, border_radius=10)

        # Text
        text_surf = font.render(self.text, True, (20, 20, 20))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    # CLICK HANDLER
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
