import pygame, random

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
        self.vx = random.choice((-5, 5))
        self.vy = random.choice((-5, 5))
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
                self.is_up = self.is_down = False
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
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.is_down:
                self.rect = self.rect.move(0, -25)
                self.is_down = False
            else:
                self.is_up = True
        else:
            self.rect = self.rect.move(0, -25)

    def dwn(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.is_up:
                self.rect = self.rect.move(0, 25)
                self.is_up = False
            else:
                self.is_down = True
        else:
            self.rect = self.rect.move(0, 25)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 2050, 1079
    screen = pygame.display.set_mode(size)
    fps = 60
    clock = pygame.time.Clock()
    Border(5, 5, width - 5, 5, False, False)
    Border(5, height - 5, width - 5, height - 5, False, False)
    Border(5, 5, 5, height - 5, False, True)
    Border(width - 5, 5, width - 5, height - 5, False, False)
    slider_l = Border(100, 450, 100, height - 450, True, True)
    slider_r = Border(width - 100, 450, width - 100, height - 450, True, True)
    Ball(20, 100, 100)
    f_up = f_dwn = False
    running = True
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
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
