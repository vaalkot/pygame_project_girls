import pygame
import sqlite3


if __name__ == '__main__':
    class Att(pygame.sprite.Sprite):
        def __init__(self, x, y, surf, group):
            pygame.sprite.Sprite.__init__(self)
            self.image = surf
            self.rect = self.image.get_rect(topleft=(x, y))
            self.add(group)

        def draw(self, sc):
            sc.blit(self.image, self.rect)

        def update(self, x, y):
            global result

            if self.rect.colliderect(pygame.Rect(x, y, 50, 50)):
                self.kill()
                result += 1


    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("super game")
    clock = pygame.time.Clock()

    con = sqlite3.connect('list_of_people_who_have_become_alexey_zhidkovsky.db')
    cur = con.cursor()

    boy1l = pygame.transform.scale(pygame.image.load('pers1_left.png').convert_alpha(), (45, 50))
    boy2l = pygame.transform.scale(pygame.image.load('pers2_left.png').convert_alpha(), (45, 50))
    boy1r = pygame.transform.scale(pygame.image.load('pers1_right.png').convert_alpha(), (45, 50))
    boy2r = pygame.transform.scale(pygame.image.load('pers2_right.png').convert_alpha(), (45, 50))
    portal = pygame.transform.scale(pygame.image.load('портал.png').convert_alpha(), (45, 50))
    girl = pygame.transform.scale(pygame.image.load('girl.png').convert_alpha(), (45, 50))

    arrow = pygame.transform.scale(pygame.image.load('стрелочка.png').convert_alpha(), (150, 100))
    usual_image = pygame.transform.scale(pygame.image.load('обычный_Глеб.png').convert_alpha(), (230, 205))
    start_image = pygame.transform.scale(pygame.image.load('веселый_Глеб.png').convert_alpha(), (230, 205))
    exit_image = pygame.transform.scale(pygame.image.load('гламур_глеб.png').convert_alpha(), (230, 205))
    final_image = pygame.transform.scale(pygame.image.load('еще_Глеб.png').convert_alpha(), (270, 245))

    images_1 = ('trousers.png', 'boots.png', 'coat.png', 'tomford.png', 'glasses.png')
    coords_1 = ((100, 0), (100, 550), (350, 451), (750, 50), (750, 515))
    surfs_1 = []
    for i in range(len(images_1)):
        surfs_1.append(pygame.transform.scale(pygame.image.load(images_1[i]).convert_alpha(), (50, 50)))

    images_2 = ('necklace.png', 'car.png', 'tickets.png', 'flowers.png')
    coords_2 = ((150, 0), (0, 550), (651, 352), (750, 0))
    surfs_2 = []
    for i in range(len(images_2)):
        surfs_2.append(pygame.transform.scale(pygame.image.load(images_2[i]).convert_alpha(), (50, 50)))

    x = 250
    y = 250
    speed = 10
    cell_size = 50
    n = 16
    result = 0


    def draw_text(text, size, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)


    def load_fon(fon_file):
        with open(fon_file, 'r') as f:
            return [list(line) for line in f.read().split('\n')]


    def can_move(x, y, fon_data):
        j, i = round(x / cell_size), round(y // cell_size)
        return 0 <= i < len(fon_data) and 0 <= j < len(fon_data[i]) and (fon_data[i][j] == '.')


    def fill_fon(screen, cell_size, n, fon_data):
        fon_dot = pygame.image.load('doroga.jpg')
        fon_plus = pygame.image.load('temno.jpg')

        for i in range(n):
            for j in range(n):
                if i < len(fon_data) and j < len(fon_data[i]):
                    if fon_data[i][j] == '.':
                        screen.blit(fon_dot, (j * cell_size, i * cell_size))
                    elif fon_data[i][j] == '+' or fon_data[i][j] == '/':
                        screen.blit(fon_plus, (j * cell_size, i * cell_size))


    def main_menu():
        while True:
            screen.fill('white')

            draw_text("cтань крашем", 55, width / 2, height / 4)
            draw_text("всех девочек!", 80, width / 2, height / 4 + 45)

            screen.blit(usual_image, (70, 320))
            screen.blit(arrow, (180, 210))

            start_button = pygame.Rect(width / 2 - 70, height / 2, 140, 50)
            pygame.draw.rect(screen, (255, 155, 204), start_button)
            draw_text("Play", 30, width / 2, height / 2 + 25)

            exit_button = pygame.Rect(width / 2 - 70, height / 2 + 60, 140, 50)
            pygame.draw.rect(screen, (255, 127, 73), exit_button)
            draw_text("Exit", 30, width / 2, height / 2 + 85)

            if start_button.collidepoint(pygame.mouse.get_pos()):
                screen.blit(start_image, (70, 320))
                pygame.draw.rect(screen, (255, 142, 204), start_button)
                draw_text("Play", 30, width / 2, height / 2 + 25)

                if click:
                    level_1(250, 250)
                    return

            if exit_button.collidepoint(pygame.mouse.get_pos()):
                screen.blit(exit_image, (70, 320))
                pygame.draw.rect(screen, (255, 117, 56), exit_button)
                draw_text("Exit", 30, width / 2, height / 2 + 85)

                if click:
                    return

            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.flip()
            pygame.time.delay(60)


    def level_1(x, y):
        fon_data = load_fon('fon1.txt')

        atts_1 = pygame.sprite.Group()

        for i in range(len(images_1)):
            Att(*coords_1[i], surfs_1[i], atts_1)

        running = True
        click = False
        side = 'l'

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            keys = pygame.key.get_pressed()

            new_x, new_y = x, y
            if keys[pygame.K_UP] and can_move(x, y - 5, fon_data):
                new_y -= speed
            if keys[pygame.K_DOWN] and can_move(x, y + 50, fon_data):
                new_y += speed
            if keys[pygame.K_LEFT] and can_move(x - 26, y, fon_data):
                side = 'l'
                new_x -= speed
            if keys[pygame.K_RIGHT] and can_move(x + 16, y, fon_data):
                side = 'r'
                new_x += speed

            x, y = new_x, new_y

            atts_1.update(x, y)

            screen.fill('white')
            fill_fon(screen, cell_size, n, fon_data)
            atts_1.draw(screen)
            screen.blit(portal, (350, 200))

            if side == 'l':
                screen.blit(boy1l, (x, y))
            else:
                screen.blit(boy1r, (x, y))

            stop_button = pygame.Rect(5, 5, 50, 50)
            pygame.draw.rect(screen, 'red', stop_button)
            draw_text("X", 60, 29, 32)

            if stop_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (204, 0, 0), stop_button)
                draw_text("X", 60, 29, 32)

                if click:
                    cur.execute('''INSERT INTO players(crush_or_not, points) VALUES(0, ?)''', (result,))
                    con.commit()
                    stop_game(1)
                    return

            if 350 <= x <= 400 and 200 <= y <= 240:
                    if result == 5:
                        level_2(0, 250)
                        return
                    else:
                        text = pygame.Rect(180, 330, 390, 90)
                        pygame.draw.rect(screen, (255, 142, 204), text)
                        draw_text("сначала соберите", 40, 375, 363)
                        draw_text("все атрибуты", 40, 375, 395)

            pygame.display.flip()
            pygame.time.delay(20)


    def level_2(x, y):
        fon_data = load_fon('fon2.txt')

        atts_2 = pygame.sprite.Group()

        for i in range(len(images_2)):
            Att(*coords_2[i], surfs_2[i], atts_2)

        running = True
        click = False
        flag = False
        side = 'l'

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            keys = pygame.key.get_pressed()

            new_x, new_y = x, y
            if keys[pygame.K_UP] and can_move(x, y - 6, fon_data):
                new_y -= speed
            if keys[pygame.K_DOWN] and can_move(x, y + 50, fon_data):
                new_y += speed
            if keys[pygame.K_LEFT] and can_move(x - 22, y, fon_data):
                side = 'l'
                new_x -= speed
            if keys[pygame.K_RIGHT] and can_move(x + 20, y, fon_data):
                side = 'r'
                new_x += speed

            x, y = new_x, new_y

            atts_2.update(x, y)

            screen.fill((0, 0, 0))
            fill_fon(screen, cell_size, n, fon_data)

            atts_2.draw(screen)
            screen.blit(girl, (750, 300))

            if side == 'l':
                screen.blit(boy2l, (x, y))
            else:
                screen.blit(boy2r, (x, y))

            stop_button = pygame.Rect(5, 5, 50, 50)
            pygame.draw.rect(screen, (255, 0, 0), stop_button)
            draw_text("X", 60, 29, 32)

            if stop_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (204, 0, 0), stop_button)
                draw_text("X", 60, 29, 32)

                if click:
                    cur.execute('''INSERT INTO players(crush_or_not, points) VALUES(0, ?)''', (result,))
                    con.commit()
                    stop_game(2)
                    return

            if 750 <= x <= 800 and 300 <= y <= 350:
                if result == 9:
                    cur.execute('''INSERT INTO players(crush_or_not, points) VALUES(1, ?)''', (result,))
                    con.commit()
                    end_game()
                    return
                else:
                    text = pygame.Rect(205, 330, 390, 90)
                    pygame.draw.rect(screen, (255, 142, 204), text)
                    draw_text("сначала соберите", 40, 400, 363)
                    draw_text("все атрибуты", 40, 400, 395)

            pygame.display.flip()
            pygame.time.delay(20)


    def stop_game(level):
        global result

        while True:
            screen.fill('white')

            draw_text("ваш результат:", 55, width / 2, height / 4)
            if level == 1:
                draw_text(f'{result}/5', 80, width / 2, height / 4 + 45)
            else:
                draw_text(f'{result}/9', 80, width / 2, height / 4 + 45)
                print(result)

            cont_but = pygame.Rect(width / 2 - 70, height / 2, 140, 50)
            pygame.draw.rect(screen, (255, 155, 204), cont_but)
            draw_text("Let's go", 30, width / 2, height / 2 + 25)

            ex_but = pygame.Rect(width / 2 - 70, height / 2 + 60, 140, 50)
            pygame.draw.rect(screen, (255, 127, 73), ex_but)
            draw_text("Exit", 30, width / 2, height / 2 + 85)

            if cont_but.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 142, 204), cont_but)
                draw_text("Let's go", 30, width / 2, height / 2 + 25)

                if click:
                    if level == 1:
                        result = 0
                        level_1(250, 250)
                    elif level == 2:
                        result = 5
                        level_2(0, 250)

            if ex_but.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 117, 56), ex_but)
                draw_text("Exit", 30, width / 2, height / 2 + 85)
                if click:
                    return

            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.flip()
            pygame.time.delay(60)


    def end_game():
        global result
        click = False

        while True:
            screen.fill('white')

            draw_text("Вы стали крашем", 55, width / 2, height / 4)
            draw_text(f'{result}/9', 80, width / 2, height / 4 + 45)

            cont_but = pygame.Rect(width / 2 - 70, height / 2, 140, 50)
            pygame.draw.rect(screen, (255, 155, 204), cont_but)
            draw_text("Еще раз!", 30, width / 2, height / 2 + 25)

            ex_but = pygame.Rect(width / 2 - 70, height / 2 + 60, 140, 50)
            pygame.draw.rect(screen, (255, 127, 73), ex_but)
            draw_text("Exit", 30, width / 2, height / 2 + 85)

            screen.blit(final_image, (510, 330))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if cont_but.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 142, 204), cont_but)
                draw_text("Еще раз!", 30, width / 2, height / 2 + 25)

                if click:
                    result = 0
                    level_1(250, 250)

            if ex_but.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 117, 56), ex_but)
                draw_text("Exit", 30, width / 2, height / 2 + 85)
                if click:
                    return

            pygame.display.flip()
            pygame.time.delay(60)

    main_menu()
    con.close()
    pygame.quit()
