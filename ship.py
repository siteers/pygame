import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self, aigame):
        super().__init__()
        #inicjalizacja statku kosmicznego i jego polozenia poczatkowego
        self.screen = aigame.screen
        self.settings = aigame.settings
        self.screen_rect = aigame.screen.get_rect()
        #każdy nowy statek kosmiczny pojawia się na dole ekranu
        self.image = pygame.image.load('1.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        #wczytywanie obrazu statku kosmicznego i pobranie jego prostokata
        
        self.x = float(self.rect.x) #wartosc zmiennoprzecinkowa (1.5) prędkości statku
        self.y = float(self.rect.y) #wartosc zmiennoprzecinkowa (1.5) prędkości statku
        
        self.moving_right = False  #jesli jest nienacisniety K_right to jest false i sie nie przesuwa
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right: #statek bedzie sie przesuwać póki wartosc bedzie mniejsza od krawedzi
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed 
        
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        #wyświetlenie statku kosmcznego w jego aktualnym polozeniu
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y) #HAHA KURWA XD
