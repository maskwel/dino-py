import pygame
import random

pygame.init()

dis_width, dis_height = 800, 600
display = pygame.display.set_mode((dis_width, dis_height))   # Задаём размер окна
pygame.display.set_caption("Dino Run")                      # Название

icon = pygame.image.load("assets/icon.png")                       # загрузка иконки окна
pygame.display.set_icon(icon)                              # размещение этой иконки возле названия

cactus_img = pygame.image.load("assets/cactus1.png")
dino_img = [pygame.image.load("assets/dino1.png"), pygame.image.load("assets/dino2.png")]

counter_dino = 0
dino_width = 70                                         # шырина и высота динозаврика
dino_height = 75
dino_x = 100                                            # позиция динозаврика
dino_y = dis_height - dino_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 20

class Cactus:
    def __init__(self, x, y, width, height, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius):
        self.x = radius

def game():
    '''основная функция игры'''

    global make_jump
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load("assets/Land.jpg")

    while game:
        for event in pygame.event.get():               # перебор всех событий
            if event.type == pygame.QUIT:
                pygame.quit()                       # блок выхода из игры
                quit()

        keys = pygame.key.get_pressed()             # перебор всех нажатых клавиш
        if keys[pygame.K_SPACE]:                    # проверка на нажатую клавишу space
            make_jump = True

        if make_jump:
            jump()
        display.blit(land, (0, 0))
        draw_array(cactus_arr)
        draw_dino()

        if check_collision(cactus_arr):
            game = False
        pygame.display.update()  # метод для обновления содержимого дисплея
        clock.tick(70)          # ограничение кадров
    return game_over()

def jump():
    '''функция прыжка динозаврика'''

    global dino_y, make_jump, jump_counter
    if jump_counter >= -20:
        dino_y -= jump_counter
        jump_counter -= 1
    else:
        jump_counter = 20
        make_jump = False

def create_cactus_arr(array):
    array.append(Cactus(dis_width + 20, dis_height - 180, 40, 80, cactus_img, 5))
    array.append(Cactus(dis_width + 400, dis_height - 180, 40, 80, cactus_img, 5))
    array.append(Cactus(dis_width + 1000, dis_height - 180, 40, 80, cactus_img, 5))
    array.append(Cactus(dis_width + 700, dis_height - 180, 40, 80, cactus_img, 5))

def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x, array[3].x)
    if maximum < dis_width:
        radius = dis_width
        if radius - maximum < 50:
            radius += 150
    else:
            radius = maximum
    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(40, 60)
    else:
        radius += random.randrange(250,1000)
    return radius

def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)
            cactus.return_self(radius)

def draw_dino():
    global counter_dino
    if counter_dino == 12:
        counter_dino = 0
    display.blit(dino_img[counter_dino // 6], (dino_x, dino_y))
    counter_dino += 1

def print_text(message, x, y, font_color=(0, 0, 0), font_size=30, font_type="fonts/play-bold.ttf"):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))

def check_collision(barriers):
    for barrier in barriers:
        if dino_y + dino_height >= barrier.y + 10:
            if barrier.x + 11 <= dino_x <= barrier.x + barrier.width:
                return True
            elif barrier.x + 11 <= dino_x + dino_width <= barrier.x + barrier.width:
                return True

def game_over():
    stop = True
    while stop:
        for event in pygame.event.get():               # перебор всех событий
            if event.type == pygame.QUIT:
                pygame.quit()                       # блок выхода из игры
                quit()
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            return True

        print_text("GAME OVER, Press Enter to restart", 160, 250)

        pygame.display.update()
        clock.tick(10)

while game():
    pass