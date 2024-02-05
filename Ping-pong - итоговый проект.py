import sys

import pygame
import random
import pygame_menu

all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
sliders = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.choice((-10, 10))
        self.vy = random.choice((-10, 10))
        self.score_left = 0
        self.score_right = 0
        balls.add(self)

    def update(self):
        font = pygame.font.Font(None, 50)
        text_l = font.render(str(self.score_left), True, (100, 255, 100))
        screen.blit(text_l, (50, 10))
        text_r = font.render(str(self.score_right), True, (100, 255, 100))
        screen.blit(text_r, (2000, 10))
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            if pygame.sprite.spritecollideany(self, vertical_borders).is_left:
                self.vx = -self.vx
                self.score_left += 1
            else:
                self.vx = -self.vx
                self.score_right += 1
        if pygame.sprite.spritecollideany(self, sliders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, is_slider, is_left):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            if is_slider:
                self.add(sliders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            else:
                self.add(vertical_borders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
                self.is_left = is_left
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def up(self):
        if self.rect.y > 0:
            self.rect = self.rect.move(0, -25)
        print(self.rect.y)

    def dwn(self):
        if self.rect.y < 900:
            self.rect = self.rect.move(0, 25)
        print(self.rect.y)

    def ai(self, x, y):
        if x < 0:
            if y > 0:
                self.dwn()
            else:
                self.up()
        else:
            self.up()

def init():
    fps = 60
    clock = pygame.time.Clock()
    Border(5, 5, width - 5, 5, False, False)
    Border(5, height - 5, width - 5, height - 5, False, False)
    Border(5, 5, 5, height - 5, False, True)
    Border(width - 5, 5, width - 5, height - 5, False, False)
    ball = Ball(20, 100, 100)
    slider_l = Border(100, 450, 100, height - 450, True, True)
    slider_r = Border(width - 100, 450, width - 100, height - 450, True, True)
    f_up = f_dwn = False
    running = True
    return ball, slider_r, slider_l, f_up, f_dwn, running, fps, clock

def start():
    ball, slider_r, slider_l, f_up, f_dwn, running, fps, clock = init()
    ai = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    f_up = True
                elif event.key == pygame.K_DOWN:
                    f_dwn = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    f_up = f_dwn = False
        if f_up:
            slider_r.up()
        elif f_dwn:
            slider_r.dwn()
        screen.fill('white')
        all_sprites.draw(screen)
        balls.update()
        if ai == 2:
            ai = 0
            slider_l.ai(ball.vx, ball.vy)
        else:
            ai += 1
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


def start_with_player(*args):
    ball, slider_r, slider_l, f_up, f_dwn, running, fps, clock = init()
    k_up = k_dwn = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    f_up = True
                elif event.key == pygame.K_DOWN:
                    f_dwn = True
                elif event.key == pygame.K_w:
                    k_up = True
                elif event.key == pygame.K_s:
                    k_dwn = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    f_up = f_dwn = False
                elif event.key in [pygame.K_w, pygame.K_s]:
                    k_up = k_dwn = False
        if f_up:
            slider_r.up()
        elif f_dwn:
            slider_r.dwn()
        if k_up:
            slider_l.up()
        elif k_dwn:
            slider_l.dwn()
        screen.fill('white')
        all_sprites.draw(screen)
        balls.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()

def for_useless_button():
    pass


if __name__ == '__main__':
    pygame.init()
    size = width, height = 2050, 1079
    screen = pygame.display.set_mode(size)
    mytheme = pygame_menu.Theme(background_color=(255, 255, 255, 255), title_background_color=(255, 0, 0), title_font_shadow=True)
    menu = pygame_menu.Menu('Welcome', 2050, 1079, theme=mytheme)
    menu.add.button('эта кнопка не видна и ничего не делает, но без неё меню не работает', for_useless_button)
    menu.add.button('Играть с машиной', start)
    menu.add.button('Играть с человеком', start_with_player)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(screen)
