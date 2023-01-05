import sys
from time import sleep
#sys - koniecznosc zakonczenia gry na żądanie 
import pygame
#pygame - funkcjonalnosc gry
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from Button import Button
from ship import Ship
from bullet import Bullet
from Alien import Alien
class AlienInvasion:
    def __init__(self): 
        pygame.init() #ustawienie tła
        self.settings = Settings() #pobieramy klase settings
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height #ustawienia rozdzielczości w settings
        pygame.display.set_caption("Alien Atacks 1.0") #nazwa gry
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self) #utworzenie egzemplarza klasy ship
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "PRESS 'b' TO PLAY")
    def run_game(self): #metoda powodujaca nieustanne dzialanie gry przez petle while
        while True:
            self._check_events() #odpalenie metody chech events - czy gracz kliknal
            if self.stats.game_active:
                self.ship.update() #odpalenie metody update z klasy ship  
                self.bullets.update()
                self._update_aliens() 
                self._update_bullets()
            self._update_screen()     
    def _check_events(self): #ta metoda jest wywolywana w petli while
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #wyswietlenie odswiezonego ekranu
                sys.exit() #koniec gry
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN: #poruszanie sie klawiatura
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP: #przesuwa sie jesli jest nacisniety, jak nie wtedy jest false
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT: #jesli nacisniemy klawisz w prawo 
            self.ship.moving_right = True #przesuwa sie jesli jest nacisniety, jak nie wtedy jest false
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_b:
            self.stats.reset_stats()
            self.stats.game_active = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    def _fire_bullet(self):
        #nowy pocisk
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)              
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color) #pobieramy kolor tła
        self.ship.blitme() #statek znajduje sie nad tłem (patrz wyzej)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip() #wyswietlenie ostatniego odswiezonego ekranu
    def _create_fleet(self):
        #pelna flota
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
            
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom() 
        

    
    def _check_fleet_edges(self): #zmiana kierunku floty jesli jest na krawedzi
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        #przesuniecie w dol
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # polozenie pociskow i usuniecie niewidocznych na ekranie
        self._check_bullet_alien_collisions()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    def _check_play_button(self, mouse_pos):
        #dziala przycisk
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
