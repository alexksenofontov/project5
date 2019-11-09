import pygame, os

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name):
    fullname = os.path.join('data', 'pics', name)
    image = pygame.image.load(fullname).convert()
    return image


def generate_level(level):
    filename = "data/levels/" + level
    map_of_level = [line.strip() for line in open(filename, 'r')]
    for i in range(len(map_of_level)):
        for j in range(len(map_of_level[i])):
            if map_of_level[i][j] == '#':
                Obj('stone', j, i)
            elif map_of_level[i][j] == '+':
                Obj('coin', j, i)


def draw_text():
    font = pygame.font.Font(None, 50)
    text = font.render('Дорожные гонки', 1, (255, 255, 0))
    screen.blit(text, (150, 100))
    pygame.draw.rect(screen, (255, 255, 0), (140, 90, text.get_width() + 20,
                                             text.get_height() + 20), 5)
    font = pygame.font.Font(None, 40)
    text = font.render('Нажмите "Пробел" для начала игры', 1, (255, 255, 0))
    screen.blit(text, (50, 200))
    running = True
    r, g, b = 0, 0, 0
    clock = pygame.time.Clock()
    k = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
        r, g = (r + 5) % 255, (g + 5) % 255
        text = font.render('Нажмите "Пробел" для начала игры', 1, (r, g, 0))
        screen.blit(text, (50, 200))
        clock.tick(15)
        pygame.display.flip()


def draw_score(score):
    font = pygame.font.Font(None, 50)
    text = font.render('Score: ' + str(score), 1, (255, 255, 0))
    screen.blit(text, (400, 20))


def draw_over():
    font = pygame.font.Font(None, 70)
    text = font.render('GAME OVER', 1, (255, 0, 0))
    screen.blit(text, (140, 250))
    pygame.draw.rect(screen, (255, 0, 0), (130, 240, text.get_width() + 20,
                                           text.get_height() + 20), 5)


def draw_win():
    font = pygame.font.Font(None, 70)
    text = font.render('YOU WIN', 1, (0, 255, 0))
    screen.blit(text, (170, 250))
    pygame.draw.rect(screen, (0, 255, 0), (160, 240, text.get_width() + 20,
                                           text.get_height() + 20), 5)


class Road(pygame.sprite.Sprite):
    image = load_image('road.jpg')

    def __init__(self, y):
        super().__init__()
        self.image = Road.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y


class Obj(pygame.sprite.Sprite):
    def __init__(self, obj_type, pos_x, pos_y):
        if obj_type == 'coin':
            super().__init__(coins_group, all_sprites)
        else:
            super().__init__(stones_group, all_sprites)
        self.obj_type = obj_type
        if obj_type == 'coin':
            self.image = 'coin.png'
        else:
            self.image = 'stone.png'
        self.image = load_image(self.image)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect().move(50 * pos_x, -50 * pos_y)


class Car(pygame.sprite.Sprite):
    image_car = load_image('car.png')
    image_car.set_colorkey(image_car.get_at((0, 0)))

    def __init__(self, group):
        super().__init__(group)
        self.image = Car.image_car
        self.rect = self.image.get_rect()
        self.rect.x = 280
        self.rect.bottom = 600


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 10

    def apply(self, obj):
        obj.rect.y += self.dy
        if obj.rect.y > 600:
            obj.rect.y = -600

    def update(self, target):
        self.dy = (target.rect.y + target.rect.h // 2 - 400) // 50


coins_group = pygame.sprite.Group()
stones_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# заставка
image = load_image('road.jpg')
screen.blit(image, (0, 0))
draw_text()
# начало игры
for y in range(-680, 5, 85):
    road = Road(y)
    all_sprites.add(road)

cars = pygame.sprite.Group()
camera = Camera()
car = Car(cars)
cars.add(car)
generate_level('level1.txt')
pygame.display.flip()
running = True
fps = 20
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.rect.x -= fps
                if car.rect.x < 0:
                    car.rect.x = 0
            if event.key == pygame.K_RIGHT:
                car.rect.x += fps
                if car.rect.x > 550:
                    car.rect.x = 550
            if event.key == pygame.K_UP:
                fps += 10
                if fps > 80:
                    fps = 80
            if event.key == pygame.K_DOWN:
                fps -= 10
                if fps < 10:
                    fps = 10
        if event.type == pygame.QUIT:
            running = False
    if score == 1000:
        draw_win()
        pygame.display.flip()
        clock.tick(1)
        running = False
    coin = pygame.sprite.spritecollideany(car, coins_group)
    stone = pygame.sprite.spritecollideany(car, stones_group)
    if coin:
        coin.rect.y = -700
        score += 10
    if stone:
        draw_over()
        pygame.display.flip()
        clock.tick(1)
        running = False
    clock.tick(fps)
    camera.update(car)
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    cars.draw(screen)
    draw_score(score)
    pygame.display.flip()

