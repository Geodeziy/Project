import os
import sys
import pygame


def load_image(name, colorkey=None):  # Функция загрузки изображения
    fullname = os.path.join('data', name)
    # Если файл не существует, то выход
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.mixer.pre_init(44100, -16, 1, 512)  # Преинитиализация музыкального плеера
pygame.init()
size = width, height = 448, 576
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
dots_group = pygame.sprite.Group()
dots = []
bigdots_group = pygame.sprite.Group()
bigdots = []

enemy1_group = pygame.sprite.Group()
enemy_wins_group = pygame.sprite.Group()
pacman_wins_group = pygame.sprite.Group()

FPS = 50
v = 25
count_dot = 0
high_score = 0
x_up = 1
level = 1
keys_active = True
image1 = False
count_FPS = 0
count1_FPS = 0
starting_activity = True
fright = False

count_of_restarts = 0
cell_size = 16
restart_capability = False

enemy_wins = 0
pacman_wins = 0


class Maze(pygame.sprite.Sprite):  # Класс лабиринта
    image = load_image("yellowcirclemaze1.png", -1)

    def __init__(self):
        super().__init__(sprite_group)
        self.image = Maze.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 0
        self.rect.y = 48


movement = ''
movement_enemy1 = ''
speed_enemy = 1


class Player(pygame.sprite.Sprite):  # Класс пакмена
    player_image = load_image('yellowcircle.png', -1)

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = Player.player_image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x  # 210
        self.rect.y = pos_y  # 410
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = (pos_x, pos_y)

    def move(self, movement0):
        global movement
        self.movement = movement0

        # print(self.rect.x, self.rect.y)

        if movement0 == 'up':
            if not pygame.sprite.collide_mask(self, maze):
                pass
                # self.rect = self.rect.move(0, -1)

            else:
                movement = ''

        if movement0 == 'down':
            if not pygame.sprite.collide_mask(self, maze):
                pass
                # self.rect = self.rect.move(0, 1)

            else:
                movement = ''

        if movement0 == 'left':
            if not pygame.sprite.collide_mask(self, maze):
                pass
                # self.rect = self.rect.move(-1, 0)

            else:
                movement = ''

        if movement0 == 'right':
            if not pygame.sprite.collide_mask(self, maze):
                pass
                # self.rect = self.rect.move(1, 0)

            else:
                movement = ''


class Enemy1(pygame.sprite.Sprite):  # Класс призрака
    image = load_image("enemy1.png", -1)

    def __init__(self, x, y):
        super().__init__(enemy1_group)
        self.image = Enemy1.image
        # self.rect = self.image.get_rect()
        self.rect = self.image.get_rect().move(16 * x + 15, 16 * y + 5)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x  # 215 226
        self.rect.y = y  # 220 256
        self.pos = (x, y)

    def move(self, movement_e):
        global keys_active
        global movement_enemy1
        global speed_enemy
        global movement
        global enemy_wins

        self.movement = movement_e

        if movement_e == 'up':
            if not pygame.sprite.collide_mask(self, maze):
                pass
                # self.rect = self.rect.move(0, -1)

            else:
                movement_enemy1 = ''
                # self.rect = self.rect.move(0, 1)
        if movement_e == 'down':
            if not pygame.sprite.collide_mask(self, maze):
                pass
                # self.rect = self.rect.move(0, 1)

            else:
                movement_enemy1 = ''
                # self.rect = self.rect.move(0, -1)
        if movement_e == 'left':
            if not pygame.sprite.collide_mask(self, maze):
                pass
                # self.rect = self.rect.move(-1, 0)

            else:
                movement_enemy1 = ''
                # self.rect = self.rect.move(1, 0)
        if movement_e == 'right':
            if not pygame.sprite.collide_mask(self, maze):
                pass
                # self.rect = self.rect.move(1, 0)

            else:
                movement_enemy1 = ''
                # self.rect = self.rect.move(-1, 0)

        if pygame.sprite.collide_mask(self, player):
            enemy_wins += 1
            music_player('pacman_death.wav')
            keys_active = False
            movement = ''
            player.kill()


class Dot(pygame.sprite.Sprite):  # Класс точки
    image = load_image("dot.png")

    def __init__(self, x, y):
        super().__init__(dots_group)
        self.image = Dot.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class BigDot(pygame.sprite.Sprite):  # Класс большой точки
    image = load_image("bigdot.png", -1)

    def __init__(self, x, y):
        super().__init__(bigdots_group)
        self.image = BigDot.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


def update(dots_list, bigdots_list):  # Функция подсчёта съеденных точек
    global count_dot
    global fright
    global speed_enemy
    global movement
    global movement_enemy1
    global pacman_wins
    global keys_active
    global restart_capability
    for i in range(len(dots_list)):
        if dots_list[i].rect.colliderect(player.rect):
            music_player('pacman_chomp.wav')
            count_dot += 10
            dots_list[i].kill()
            dots_list[i].rect.x = -1
            dots_list[i].rect.y = -1
    for j in range(len(bigdots_list)):
        if bigdots_list[j].rect.colliderect(player.rect):
            music_player('pacman_intermission.wav')
            count_dot += 50
            enemy1.image = load_image('enemy-fright.png', -1)
            fright = True
            speed_enemy += 2
            bigdots_list[j].kill()
            bigdots_list[j].rect.x = -1
            bigdots_list[j].rect.y = -1

    if (not dots_group and not bigdots_group):
        keys_active = False
        restart_capability = True
        movement = ''
        movement_enemy1 = ''


def moving(y_circle, movement0):  # Функция передвижения пакмена
    global movement
    x, y = y_circle.pos

    if player.rect.x < 0:
        player.rect.x = 448
        player.rect.y = 270
        movement0 = 'left'

    if player.rect.x > 448:
        player.rect.x = -1
        player.rect.y = 270
        movement0 = 'right'

    if movement0 == 'up':
        if not image1:
            player.image = load_image('pacman-up.png', -1)
        if image1:
            player.image = load_image('pacman-up-1.png', -1)
        if not pygame.sprite.collide_mask(player, maze):
            player.rect = player.rect.move(0, -1)
            # y -= int(v / FPS)
        else:
            movement = ''
            player.image = load_image('yellowcircle.png', -1)
            player.rect = player.rect.move(0, 1)
    if movement0 == 'down':
        if not image1:
            player.image = load_image('pacman-down.png', -1)
        if image1:
            player.image = load_image('pacman-down-1.png', -1)
        if not pygame.sprite.collide_mask(player, maze):
            player.rect = player.rect.move(0, 1)
            # y += int(v / FPS)
        else:
            movement = ''
            player.image = load_image('yellowcircle.png', -1)
            player.rect = player.rect.move(0, -1)
    if movement0 == 'left':
        if not image1:
            player.image = load_image('pacman-left.png', -1)
        if image1:
            player.image = load_image('pacman-left-1.png', -1)
        if not pygame.sprite.collide_mask(player, maze):
            player.rect = player.rect.move(-1, 0)
            # x -= int(v / FPS)
        else:
            movement = ''
            player.image = load_image('yellowcircle.png', -1)
            player.rect = player.rect.move(1, 0)
    if movement0 == 'right':
        if not image1:
            player.image = load_image('pacman-right.png', -1)
        if image1:
            player.image = load_image('pacman-right-1.png', -1)
        if not pygame.sprite.collide_mask(player, maze):
            player.rect = player.rect.move(1, 0)
            # x += int(v / FPS)
        else:
            movement = ''
            player.image = load_image('yellowcircle.png', -1)
            player.rect = player.rect.move(-1, 0)


def moving_enemy(enemy, movement0):  # Функция передвижения и соприкосновения призрака
    global speed_enemy
    global movement_enemy1
    global movement
    global keys_active
    global restart_capability
    global fright
    global pacman_wins
    global enemy_wins
    global count1_FPS
    global count_dot
    x, y = enemy.pos

    if fright and count1_FPS == 12250:
        count1_FPS = 0
        fright = False
        speed_enemy = 1

    if enemy1.rect.x < 0:
        enemy1.rect.x = 448
        enemy1.rect.y = 270
        movement0 = 'left'

    if enemy1.rect.x > 448:
        enemy1.rect.x = -1
        enemy1.rect.y = 270
        movement0 = 'right'

    if movement0 == 'up':
        if not image1:
            enemy1.image = load_image('enemy1-up.png', -1)
        if image1:
            enemy1.image = load_image('enemy1-up-1.png', -1)

        if fright:
            if not image1:
                enemy1.image = load_image('enemy-fright.png', -1)
            if image1:
                enemy1.image = load_image('enemy-fright-1.png', -1)
        if not pygame.sprite.collide_mask(enemy1, maze):
            # enemy1.image = load_image('enemy1-up.png', -1)
            enemy1.rect = enemy1.rect.move(0, -speed_enemy)
            # y -= int(v / FPS)
        else:
            movement_enemy1 = ''

            enemy1.rect = enemy1.rect.move(0, speed_enemy)
    if movement0 == 'down':
        if not image1:
            enemy1.image = load_image('enemy1-down.png', -1)
        if image1:
            enemy1.image = load_image('enemy1-down-1.png', -1)

        if fright:
            if not image1:
                enemy1.image = load_image('enemy-fright.png', -1)
            if image1:
                enemy1.image = load_image('enemy-fright-1.png', -1)
        if not pygame.sprite.collide_mask(enemy1, maze):
            # enemy1.image = load_image('enemy1-down.png', -1)
            enemy1.rect = enemy1.rect.move(0, speed_enemy)
            # y += int(v / FPS)
        else:
            movement_enemy1 = ''

            enemy1.rect = enemy1.rect.move(0, -speed_enemy)
    if movement0 == 'left':
        if not image1:
            enemy1.image = load_image('enemy1-left.png', -1)
        if image1:
            enemy1.image = load_image('enemy1-left-1.png', -1)

        if fright:
            if not image1:
                enemy1.image = load_image('enemy-fright.png', -1)
            if image1:
                enemy1.image = load_image('enemy-fright-1.png', -1)
        if not pygame.sprite.collide_mask(enemy1, maze):
            # enemy1.image = load_image('enemy1-left.png', -1)
            enemy1.rect = enemy1.rect.move(-speed_enemy, 0)
            # x -= int(v / FPS)
        else:
            movement_enemy1 = ''

            enemy1.rect = enemy1.rect.move(speed_enemy, 0)
    if movement0 == 'right':
        if not image1:
            enemy1.image = load_image('enemy1-right.png', -1)
        if image1:
            enemy1.image = load_image('enemy1-right-1.png', -1)

        if fright:
            if not image1:
                enemy1.image = load_image('enemy-fright.png', -1)
            if image1:
                enemy1.image = load_image('enemy-fright-1.png', -1)
        if not pygame.sprite.collide_mask(enemy1, maze):
            # enemy1.image = load_image('enemy1-right.png', -1)
            enemy1.rect = enemy1.rect.move(speed_enemy, 0)
            # x += int(v / FPS)
        else:
            movement_enemy1 = ''

            enemy1.rect = enemy1.rect.move(-speed_enemy, 0)

    if pygame.sprite.collide_mask(enemy1, player):
        if not fright:
            music_player('pacman_death.wav')
            enemy_wins += 1
            keys_active = False
            restart_capability = True
            player.rect.x = -1
            player.rect.y = -1
            movement = ''
            movement_enemy1 = ''
            player.kill()
        else:
            music_player('pacman_eatghost.wav')
            pacman_wins += 1
            count_dot += 200
            restart_capability = True
            fright = False
            keys_active = False
            movement = ''
            enemy1.rect.x = -1
            enemy1.rect.y = -1
            enemy1.kill()


def start_screen():  # Функция стартовой заставки
    music_player('pacman_beginning.wav')
    fon = pygame.transform.scale(load_image('startscreen.png'), size)
    screen.blit((fon), (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def counting():  # Функция вывода количеств очков за съеденные точки, количеств выигрышей призрака и пакмена
    global high_score
    global x_up
    global enemy_wins
    global pacman_wins
    if count_dot > high_score:
        high_score = count_dot
    intro_text = [f"{x_up}UP    HIGH SCORE", f"  {count_dot}                  {high_score}"]
    font = pygame.font.Font(None, 14)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, True, (222, 222, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    if enemy_wins == 1:
        enemy_w = pygame.sprite.Sprite()
        enemy_w.image = load_image("enemy-m.png")
        enemy_w.rect = enemy_w.image.get_rect()
        enemy_w.rect.x = 190
        enemy_w.rect.y = 16
        enemy_wins_group.add(enemy_w)

    elif enemy_wins == 2:
        enemy_w2 = pygame.sprite.Sprite()
        enemy_w2.image = load_image("enemy-m.png")
        enemy_w2.rect = enemy_w2.image.get_rect()
        enemy_w2.rect.x = 210
        enemy_w2.rect.y = 16
        enemy_wins_group.add(enemy_w2)

    elif enemy_wins == 3:
        enemy_w3 = pygame.sprite.Sprite()
        enemy_w3.image = load_image("enemy-m.png")
        enemy_w3.rect = enemy_w3.image.get_rect()
        enemy_w3.rect.x = 230
        enemy_w3.rect.y = 16
        enemy_wins_group.add(enemy_w3)

    if pacman_wins == 1:
        pacman_w1 = pygame.sprite.Sprite()
        pacman_w1.image = load_image("pacman-m.png", -1)
        pacman_w1.rect = pacman_w1.image.get_rect()
        pacman_w1.rect.x = 250
        pacman_w1.rect.y = 16
        enemy_wins_group.add(pacman_w1)

    elif pacman_wins == 2:
        pacman_w2 = pygame.sprite.Sprite()
        pacman_w2.image = load_image("pacman-m.png", -1)
        pacman_w2.rect = pacman_w2.image.get_rect()
        pacman_w2.rect.x = 270
        pacman_w2.rect.y = 16
        enemy_wins_group.add(pacman_w2)

    elif pacman_wins == 3:
        pacman_w3 = pygame.sprite.Sprite()
        pacman_w3.image = load_image("pacman-m.png", -1)
        pacman_w3.rect = pacman_w3.image.get_rect()
        pacman_w3.rect.x = 290
        pacman_w3.rect.y = 16
        enemy_wins_group.add(pacman_w3)


def load_level(filename):  # Функция загрузки уровня
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def music_player(musicname):  # Функция звуков и музыки
    pygame.mixer.init()
    if musicname == 'pacman_chomp.wav':
        pygame.mixer.music.load(os.path.join('data', musicname))
        pygame.mixer.music.play()
    else:
        pygame.mixer.Sound(os.path.join('data', musicname)).play()


def win(a):  # Функция вывода текста выигрыша
    if a == 'enemy':
        intro_text = [f"ПРИЗРАК ВЫИГРАЛ"]
        font = pygame.font.Font(None, 16)
        text_coord = 170
        for line in intro_text:
            string_rendered = font.render(line, True, (255, 0, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 170
            intro_rect.y = 320
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    if a == 'pacman':
        intro_text = [f"ПАКМЕН ВЫИГРАЛ"]
        font = pygame.font.Font("C:\WINDOWS\Fonts\ARIALN.TTF", 16)
        text_coord = 170
        for line in intro_text:
            string_rendered = font.render(line, True, (255, 255, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 170
            intro_rect.y = 320
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)


if __name__ == '__main__':
    pygame.display.set_icon(load_image('icon.png'))
    pygame.display.set_caption('Пакмен и призрак')
    running = True
    start_screen()
    clock = pygame.time.Clock()
    maze = Maze()

    dots_c = [[182, 470], [86, 374], [310, 518], [422, 70], [422, 134], [182, 70], [150, 166], [182, 134], [422, 390],
              [150, 422], [54, 470], [310, 374], [422, 518], [182, 518], [422, 118], [278, 70], [150, 150], [422, 182],
              [246, 374], [182, 182], [278, 134], [246, 502], [422, 374], [182, 374], [214, 134], [422, 502],
              [150, 470], [310, 422], [278, 518], [246, 102], [150, 70], [422, 166], [150, 134], [246, 422], [278, 182],
              [246, 486], [374, 470], [278, 374], [150, 454], [422, 486], [150, 518], [406, 422], [246, 86], [374, 70],
              [374, 134], [150, 182], [246, 406], [246, 470], [150, 374], [374, 518], [150, 438], [70, 70], [278, 422],
              [70, 134], [406, 470], [246, 70], [246, 134], [102, 86], [374, 182], [102, 150], [102, 214], [342, 342],
              [70, 518], [102, 278], [246, 390], [102, 342], [342, 406], [342, 470], [102, 406], [246, 518], [374, 374],
              [102, 470], [406, 134], [198, 102], [70, 182], [342, 70], [246, 118], [406, 518], [342, 134], [102, 70],
              [246, 182], [342, 198], [70, 374], [102, 134], [342, 262], [102, 198], [198, 422], [102, 262], [342, 326],
              [198, 486], [102, 326], [342, 390], [280, 470], [102, 390], [342, 454], [342, 518], [102, 454], [406, 70],
              [406, 182], [102, 518], [406, 374], [198, 86], [342, 118], [342, 182], [102, 118], [342, 246], [102, 182],
              [198, 406], [38, 518], [102, 246], [198, 470], [102, 310], [342, 310], [342, 374], [102, 374], [342, 438],
              [102, 438], [198, 70], [38, 182], [198, 134], [342, 102], [342, 166], [102, 102], [38, 374], [342, 230],
              [102, 166], [166, 422], [70, 470], [102, 230], [198, 390], [102, 294], [342, 294], [134, 70], [102, 358],
              [198, 518], [134, 134], [102, 422], [342, 358], [342, 422], [262, 182], [294, 70], [198, 118], [86, 182],
              [262, 374], [198, 182], [294, 134], [342, 86], [134, 518], [342, 150], [342, 214], [38, 422], [198, 374],
              [342, 278], [166, 470], [294, 454], [198, 502], [294, 518], [166, 70], [134, 374], [166, 134], [262, 422],
              [294, 182], [390, 470], [38, 470], [294, 374], [294, 438], [22, 406], [166, 518], [22, 470], [390, 70],
              [38, 70], [390, 134], [38, 134], [22, 70], [134, 422], [166, 182], [22, 134], [294, 166], [262, 470],
              [390, 454], [118, 422], [166, 374], [390, 518], [294, 422], [22, 390], [262, 70], [22, 518], [262, 134],
              [390, 182], [326, 518], [294, 150], [22, 118], [390, 374], [22, 182], [358, 470], [262, 518], [390, 438],
              [22, 374], [294, 470], [22, 502], [358, 70], [326, 374], [118, 70], [358, 134], [118, 134], [22, 166],
              [390, 422], [358, 518], [54, 70], [118, 518], [54, 134], [22, 486], [230, 134], [326, 422], [358, 182],
              [54, 454], [54, 518], [22, 86], [358, 374], [22, 150], [118, 374], [230, 518], [86, 470], [214, 518],
              [54, 182], [86, 70], [54, 374], [86, 134], [54, 438], [182, 422], [326, 70], [86, 518], [422, 86],
              [326, 134], [422, 150], [310, 70], [310, 134], [422, 406], [54, 422], [422, 470]]

    dots = [Dot(dots_c[i][0], dots_c[i][1]) for i in range(len(dots_c))]  # 240 точек

    bigdots = [BigDot(16, 96), BigDot(416, 96), BigDot(416, 416), BigDot(16, 416)]

    player = Player(210, 410)
    enemy1 = Enemy1(215, 220)

    door = pygame.sprite.Sprite()
    door.image = load_image("door.png")
    door.rect = door.image.get_rect()
    door_mask = pygame.mask.from_surface(door.image)
    door.rect.x = 208
    door.rect.y = 250
    sprite_group.add(door)
    level_map = load_level('map.txt')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # Перемещение пакмена и призрака
                if (event.key == pygame.K_w) and keys_active:
                    Player.move(player, 'up')
                    movement = 'up'
                if (event.key == pygame.K_a) and keys_active:
                    Player.move(player, 'left')
                    movement = 'left'
                if (event.key == pygame.K_s) and keys_active:
                    Player.move(player, 'down')
                    movement = 'down'
                if (event.key == pygame.K_d) and keys_active:
                    Player.move(player, 'right')
                    movement = 'right'

                if (event.key == pygame.K_RIGHT) and keys_active:
                    Enemy1.move(enemy1, 'right')
                    movement_enemy1 = 'right'
                if (event.key == pygame.K_DOWN) and keys_active:
                    Enemy1.move(enemy1, 'down')
                    movement_enemy1 = 'down'
                if (event.key == pygame.K_LEFT) and keys_active:
                    Enemy1.move(enemy1, 'left')
                    movement_enemy1 = 'left'
                if (event.key == pygame.K_UP) and keys_active:
                    Enemy1.move(enemy1, 'up')
                    movement_enemy1 = 'up'

                if (((not dots_group and not bigdots_group) or restart_capability) and (
                        restart_capability and event.key == pygame.K_ESCAPE)) and (pacman_wins < 3 and enemy_wins < 3):
                    # Перезапуск
                    count_of_restarts += 1
                    if (not dots_group and not bigdots_group):
                        pacman_wins += 1

                    keys_active = True
                    enemy1.kill()
                    enemy1.rect.x = -1
                    enemy1.rect.y = -1
                    player.kill()
                    player.rect.x = -1
                    player.rect.y = -1
                    count_dot = 0

                    for i in range(len(dots)):
                        dots[i].kill()
                        dots[i].rect.x = -1
                        dots[i].rect.y = -1
                    for j in range(len(bigdots)):
                        bigdots[j].kill()
                        bigdots[j].rect.x = -1
                        bigdots[j].rect.y = -1

                    fright = False
                    speed_enemy = 1
                    dots = [Dot(dots_c[i][0], dots_c[i][1]) for i in range(len(dots_c))]
                    bigdots = [BigDot(16, 96), BigDot(416, 96), BigDot(416, 416), BigDot(16, 416)]
                    player = Player(210, 410)
                    enemy1 = Enemy1(215, 220)

        screen.fill(pygame.Color('black'))
        counting()
        moving(player, movement)
        moving_enemy(enemy1, movement_enemy1)

        update(dots, bigdots)
        sprite_group.draw(screen)
        player_group.draw(screen)
        if not image1 and count_FPS == FPS * 8:
            image1 = True
            count_FPS = 0
        elif image1 and count_FPS == FPS * 8:
            image1 = False
            count_FPS = 0
        # Enemy1.move(enemy1)
        enemy1_group.draw(screen)
        dots_group.draw(screen)
        bigdots_group.draw(screen)

        enemy_wins_group.draw(screen)
        pacman_wins_group.draw(screen)
        clock.tick(FPS)
        count_FPS += FPS
        if fright:
            count1_FPS += FPS

        if (pacman_wins == 3 or enemy_wins == 3):  # Надпись чей выигрыш
            keys_active = False
            movement = ''
            movement_enemy1 = ''
            if enemy_wins == 3:
                win('enemy')
            elif pacman_wins == 3:
                win('pacman')

        pygame.display.flip()

    pygame.quit()
