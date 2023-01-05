import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #klasa obcego
    def __init__(self, aigame):
        #polozenie i utworzenie obcego
        super().__init__()
        self.screen = aigame.screen
        self.settings = aigame.settings

        #wczytanie obrazu obcego
        self.image = pygame.image.load("k2.bmp")
        self.rect = self.image.get_rect()

        #umieszczebue ibcego w poblizu rogu
        self.rect.x =  self.rect.width
        self.rect.y = self.rect.height
        #przechowywanie dokladnego polozenia poziomego obcego
        self.x = float(self.rect.x)

    def update(self):
        #przesuniecie obecego w prawo i lewo
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        #zwraca wartosc true jesli obcy znajduje sie przy krawedzi ekranu
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

