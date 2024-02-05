import pygame
import random
import pygame_menu

all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()    # игрок
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()    # границы
sliders = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):   # класс мяча
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.choice((-10, 10))
        self.vy = random.choice((-10, 10))    # направление мяча
        self.score_left = 0
        self.score_right = 0    # счёт
        self.sound = pygame.mixer.Sound('Sound_knock.mp3')
        self.sound.set_volume(0.3)
        file = open('record.txt', 'r')
        self.records = list(file.read())
        print(self.records)
        file.close()
        balls.add(self)

    def update(self):
        font = pygame.font.Font(None, 50)
        text_l = font.render(f'{str(self.score_left)} рекорд:{self.records[1]}', True, (100, 255, 100))
        screen.blit(text_l, (60, 10))
        text_r = font.render(f'рекорд:{self.records[0]} {str(self.score_right)}', True, (100, 255, 100))
        screen.blit(text_r, (1570, 10))     # отрисовка счёта
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):    # столкновение с границей поля
            self.vy = -self.vy
            self.sound.play()
        if pygame.sprite.spritecollideany(self, vertical_borders):    # обновление счёта
            if pygame.sprite.spritecollideany(self, vertical_borders).is_left:
                self.vx = -self.vx
                self.score_right += 1
                self.sound.play()
            else:
                self.vx = -self.vx
                self.score_left += 1
                self.sound.play()
        elif pygame.sprite.spritecollideany(self, sliders):    # столкновение с игроком
            if pygame.sprite.spritecollideany(self, sliders).is_left and self.vx < 0:
                self.vx = -self.vx
                self.sound.play()
            elif not pygame.sprite.spritecollideany(self, sliders).is_left and self.vx > 0:
                self.vx = -self.vx
                self.sound.play()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, is_slider, is_left):
        super().__init__(all_sprites)
        if x1 == x2:
            if is_slider:   # игрок
                self.add(sliders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
                self.is_left = is_left
            else:   # вертикальная стенка
                self.add(vertical_borders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
                self.is_left = is_left
        else:   # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def up(self):   # перемещение вверх
        if self.rect.y > 0:
            self.rect = self.rect.move(0, -25)
        print(self.rect.y)

    def dwn(self):   # перемещение вниз
        if self.rect.y < 900:
            self.rect = self.rect.move(0, 25)
        print(self.rect.y)

    def ai(self, x, y):   # поведение машины
        if x < 0:
            if y > 0:
                self.dwn()
            else:
                self.up()
        else:
            self.up()


def init():
    menu.close()    # создание поля
    fps = 60
    clock = pygame.time.Clock()
    Border(5, 5, width - 5, 5, False, False)
    Border(5, height - 5, width - 5, height - 5, False, False)
    Border(5, 5, 5, height - 5, False, True)
    Border(width - 5, 5, width - 5, height - 5, False, False)
    ball = Ball(20, 1025, 539)
    slider_l = Border(100, 450, 100, height - 450, True, True)
    slider_r = Border(width - 100, 450, width - 100, height - 450, True, False)
    pygame.mixer.music.load('bg_sound2.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    f_up = f_dwn = False
    running = True
    return ball, slider_r, slider_l, f_up, f_dwn, running, fps, clock


def start():   # игра с машиной
    ball, slider_r, slider_l, f_up, f_dwn, running, fps, clock = init()
    ai = 0
    image_1 = pygame.image.load('lose.png')
    image_1.set_colorkey(image_1.get_at((0, 0)))
    image_1 = pygame.transform.scale(image_1, (40, 50))
    image_2 = pygame.image.load('machine.png')
    image_2.set_colorkey(image_2.get_at((0, 0)))
    image_2 = pygame.transform.scale(image_2, (40, 50))
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
        if f_up:   # движение игрока
            slider_r.up()
        elif f_dwn:
            slider_r.dwn()
        screen.fill('white')
        screen.blit(image_2, (10, 10))
        screen.blit(image_1, (2000, 10))
        all_sprites.draw(screen)
        balls.update()
        if ai == 2:   # движение машины
            ai = 0
            slider_l.ai(ball.vx, ball.vy)
        else:
            ai += 1
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


def start_with_player(*args):   # игра с человеком
    ball, slider_r, slider_l, f_up, f_dwn, running, fps, clock = init()
    k_up = k_dwn = False
    image_1 = pygame.image.load('lose.png')
    image_1.set_colorkey(image_1.get_at((0, 0)))
    image_1 = pygame.transform.scale(image_1, (40, 50))
    image_2 = pygame.image.load('strong.png')
    image_2.set_colorkey(image_2.get_at((0, 0)))
    image_2 = pygame.transform.scale(image_2, (40, 50))
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
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        if ball.score_right == ball.score_left:
            screen.blit(image_2, (10, 10))
            screen.blit(image_2, (2000, 10))
        elif ball.score_right < ball.score_left:
            screen.blit(image_2, (10, 10))
            screen.blit(image_1, (2000, 10))
        elif ball.score_right > ball.score_left:
            screen.blit(image_1, (10, 10))
            screen.blit(image_2, (2000, 10))
        balls.update()
        clock.tick(fps)
        pygame.display.flip()
    with open("record.txt", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            records = list(line)
            if ball.score_right > int(records[0]):
                f.write(str(ball.score_right) + str(records[1]))
            if ball.score_left > int(records[1]):
                f.write(str(records[0]) + str(ball.score_left))
        f.truncate()
    pygame.quit()


def for_useless_button():
    pass


if __name__ == '__main__':
    pygame.init()
    size = width, height = 2050, 1079
    screen = pygame.display.set_mode(size)
    mytheme = pygame_menu.Theme(background_color=(255, 255, 255, 255), title_background_color=(255, 0, 0))      # Главное меню
    menu = pygame_menu.Menu('Добро пожаловать', 2050, 1079, theme=mytheme)
    menu.add.button('', for_useless_button)    # эта кнопка не видна и ничего не делает, но без неё меню не работает
    menu.add.button('Играть с машиной', start)
    menu.add.button('Играть с человеком', start_with_player)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(screen)
