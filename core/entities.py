import pygame
import math
import os

# memuat gambar
def load_image(path, size):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, size)
    return None

class Robot:
    def __init__(self, start_pos):
        self.pos = list(start_pos)  
        self.speed = 5
        
        self.image = load_image("assets/images/robot.png", (36, 36))

    def move_towards(self, target_pos):
        tx, ty = target_pos
        rx, ry = self.pos
        dist = math.hypot(tx - rx, ty - ry)
        
        if dist <= self.speed:
            self.pos = [tx, ty]
            return True 
        else:
            dx = (tx - rx) / dist
            dy = (ty - ry) / dist
            self.pos[0] += dx * self.speed
            self.pos[1] += dy * self.speed
            return False

    def draw(self, screen):
        if self.image:
            
            rect = self.image.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, (0, 0, 255), (int(self.pos[0]), int(self.pos[1])), 18)


class Victim:
    def __init__(self, pos):
        self.pos = pos
        self.is_rescued = False
        self.image = load_image("assets/images/victim.png", (34, 34))

    def draw(self, screen):
        if not self.is_rescued:
            if self.image:
                rect = self.image.get_rect(center=self.pos)
                screen.blit(self.image, rect)
            else:
                pygame.draw.circle(screen, (255, 0, 0), self.pos, 18)