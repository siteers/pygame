import pygame.font

class Button():
    def __init__(self, aigame, msg):
        self.screen = aigame.screen
        self.screen_rect = self.screen.get_rect()

#zdefinionwanie wymiarow i wls przycisku
        self.width, self.height = 200, 50
        self.button_color = (0, 125, 0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
# utworzenie prostokata przycisku i wysrodkowanie go
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center
# komunikat wyswietlany przez przycisk trzeba przygotowac tylko jednokrotnie
        self._prep_msg(msg)
    def _prep_msg(self, msg):
        #umeiszczanie komunikatu w wygenerowanym obrazie i wysrodkowanie tekstu na rpzycisku
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)