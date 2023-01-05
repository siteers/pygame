import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #klasa do pociskow
    def __init__(self, aigame):
        #utworzenie pocisku w aktualnym polozeniu statku
        super().__init__()
        self.screen = aigame.screen
        self.settings = aigame.settings
        self.color = self.settings.bullet_color

        #utworzenie pocisku w 0,0, zdefiniowanie jego polozenia
        
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height) #to robimy poniewaz pocisk nie jest zdjeciem
        self.rect.midtop = aigame.ship.rect.midtop #polozenie pocisku jak statku

        self.y = float(self.rect.y)

    def update(self):
        #poruszanie statkiem
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)