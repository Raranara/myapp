import random
import pygame
import sys
import struct


class InputBox:  # класс для ввода данных

    def __init__(self, x, y, w, h, text=''):  # x, y, w, h - координаты
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.poss = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):  # если кликнули на него
                # Toggle the active variable.
                if not self.active and self.poss:
                    self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            if self.poss:
                self.color = (0, 255, 0) if self.active else (255, 255, 255)
            else:
                self.color = (0, 0, 0)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = (0, 0, 0)
                    self.poss = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)



def formula(w):
    return ((w * 2 - 1) // 2 + 1) * width_line + ((w * 2 - 1) // 2) * width_walls + border * 2

def labyrinth_name():
    global width_window, height_window
    clock = pygame.time.Clock()
    f2 = pygame.font.SysFont('serif', 25)
    text = "Введите имя лабиринта:"
    point_numb = f2.render(text, True, (255,255,255))
    place_numb = point_numb.get_rect(center=(width_window // 2, height_window / 8))
    input_box1 = InputBox(100, 150, 140, 32)
    input_boxes = [input_box1]
    done = False
    while not done:
        for event in pygame.event.get():
            if (not input_box1.poss) or event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        window.fill((30, 30, 30))
        window.blit(point_numb, place_numb)
        for box in input_boxes:
            box.draw(window)

        pygame.display.flip()
        clock.tick(30)
    return input_box1.text




def pack_matrix(g):
    ans = []
    a = ''
    for i in g:
        for j in i:
            if j == 1:
                a += '1'
            else:
                a += '0'
            if len(a) == 7:
                #print(a[::-1])
                a += '1'
                ans.append(int(a[::-1], 2))

                a = ''
    if a != '':
        #print(a[::-1])
        a += '1'
        ans.append(int(a[::-1], 2))
    return ans


def start_point_generate(n, m):
    if random.choice([1, 0]):
        if random.choice([1, 0]):
            start = (0, random.randint(0, m - 1))
        else:
            start = (n - 1, random.randint(0, m - 1))
    else:
        if random.choice([1, 0]):
            start = (random.randint(0, n - 1), 0)
        else:
            start = (random.randint(0, n - 1), m - 1)
    return start


def finish_point_generate(start, n, m):
    return n - 1 - start[0], m - 1 - start[1]


def transition_choice(x, y, rm):
    choice_list = []
    if x > 0:
        if not rm[x - 1][y]:
            choice_list.append((x - 1, y))
    if x < len(rm) - 1:
        if not rm[x + 1][y]:
            choice_list.append((x + 1, y))
    if y > 0:
        if not rm[x][y - 1]:
            choice_list.append((x, y - 1))
    if y < len(rm[0]) - 1:
        if not rm[x][y + 1]:
            choice_list.append((x, y + 1))
    if choice_list:
        nx, ny = random.choice(choice_list)
        if x == nx:
            if ny > y:
                tx, ty = x * 2, ny * 2 - 1
            else:
                tx, ty = x * 2, ny * 2 + 1
        else:
            if nx > x:
                tx, ty = nx * 2 - 1, y * 2
            else:
                tx, ty = nx * 2 + 1, y * 2
        return nx, ny, tx, ty
    else:
        return -1, -1, -1, -1


def create_labyrinth(n, m):
    reach_matrix = []
    for i in range(n):
        reach_matrix.append([])
        for j in range(m):
            reach_matrix[i].append(0)
    transition_matrix = []
    for i in range(n * 2 - 1):
        transition_matrix.append([])
        for j in range(m * 2 - 1):
            if i % 2 == 0 and j % 2 == 0:
                transition_matrix[i].append(1)
            else:
                transition_matrix[i].append(0)
    start = start_point_generate(n, m)
    finish = finish_point_generate(start, n, m)
    list_transition = [start]
    x, y = start
    reach_matrix[x][y] = 1
    x, y, tx, ty = transition_choice(x, y, reach_matrix)
    for i in range(1, m * n):
        while not (x >= 0 and y >= 0):
            x, y = list_transition[-1]
            list_transition.pop()
            x, y, tx, ty = transition_choice(x, y, reach_matrix)
        reach_matrix[x][y] = 1
        list_transition.append((x, y))
        transition_matrix[tx][ty] = 1
        x, y, tx, ty = transition_choice(x, y, reach_matrix)
    return transition_matrix, start, finish


def draw_labyrinth(matrix, start, finish, width_line=20, width_walls=5, color_way=(255, 255, 255),
                   color_wall=(0, 0, 0),
                   border=5, color_start=(0, 255, 0), color_finish=(255, 0, 0)):
    ww = (len(matrix) // 2 + 1) * width_line + (len(matrix) // 2) * width_walls + border * 2
    hh = (len(matrix[0]) // 2 + 1) * width_line + (len(matrix[0]) // 2) * width_walls + border * 2
    for ii in range(ww):
        for j in range(hh):
            if ii < border or ww - ii <= border or j < border or hh - j <= border:
                pygame.draw.line(window, color_wall, [ii, j], [ii, j], 1)
            else:
                if (ii - border) % (width_line + width_walls) <= width_line:
                    xx = (ii - border) // (width_line + width_walls) * 2
                else:
                    xx = (ii - border) // (width_line + width_walls) * 2 + 1
                if (j - border) % (width_line + width_walls) <= width_line:
                    y = (j - border) // (width_line + width_walls) * 2
                else:
                    y = (j - border) // (width_line + width_walls) * 2 + 1
                if matrix[xx][y]:
                    pygame.draw.line(window, color_way, [ii, j], [ii, j], 1)
                else:
                    pygame.draw.line(window, color_wall, [ii, j], [ii, j], 1)
    pygame.draw.rect(window, color_start, (
        border + start[0] * (width_line + width_walls), border + start[1] * (width_line + width_walls), width_line,
        width_line))
    pygame.draw.rect(window, color_finish, (
        border + finish[0] * (width_line + width_walls), border + finish[1] * (width_line + width_walls), width_line,
        width_line))



border = 5
width_line = 30
width_walls = 20
color_way = (255, 255, 255)
color_wall = (0, 0, 0)
color_start = (0, 255, 0)
color_finish = (255, 0, 0)
width = random.randint(5, 12)
height = width
width_window = max(300, formula(width))
height_window = max(300, formula(height))
matrix_base = []


pygame.init()


window = pygame.display.set_mode((width_window, height_window + 70))
pygame.display.set_caption("Labyrinth")
pygame.display.set_icon(pygame.image.load("icon.png"))
font = pygame.font.Font(None, 25)
matrix, start, finish = create_labyrinth(width, height)
draw_labyrinth(matrix, start, finish, width_line, width_walls, color_way,
               color_wall,
               border, color_start, color_finish)
text3 = font.render("ЛКМ - след.лабиринт", True, (255, 255, 255))
text2 = font.render("L - загрузить лабиринт", True, (255, 255, 255))
text1 = font.render("S - сохранить лабиринт", True, (255, 255, 255))
window.blit(text3, (10, height_window))
window.blit(text2, (10, height_window + 20))
window.blit(text1, (10, height_window + 40))
pygame.display.update()


while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                window = pygame.display.set_mode((width_window, height_window + 70))
                window.fill((0, 0, 0))
                pygame.draw.rect(window, (0, 0, 0), (0, height_window - 70, width_window, 70))
                matrix, start, finish = create_labyrinth(width, height)
                draw_labyrinth(matrix, start, finish, width_line, width_walls, color_way,
                               color_wall,
                               border, color_start, color_finish)
                text3 = font.render("ЛКМ - след.лабиринт", True, (255, 255, 255))
                text2 = font.render("L - загрузить лабиринт", True, (255, 255, 255))
                text1 = font.render("S - сохранить лабиринт", True, (255, 255, 255))
                window.blit(text3, (10, height_window))
                window.blit(text2, (10, height_window + 20))
                window.blit(text1, (10, height_window + 40))
                pygame.display.update()


        if i.type == pygame.KEYUP:
            if i.key == pygame.K_s:
                name = labyrinth_name()
                with open((name + ".rara"), "wb") as file:
                    data = struct.pack('<b', 114)
                    data += struct.pack('<b', 97)
                    data += struct.pack('<b', 114)
                    data += struct.pack('<b', 97)
                    data += struct.pack('<b', width * 2 - 1)
                    data += struct.pack('<b', height * 2 - 1)
                    data += struct.pack('<b', start[0])
                    data += struct.pack('<b', start[1])
                    data += struct.pack('<b', finish[0])
                    data += struct.pack('<b', finish[1])
                    file.write(data)
                    for x in pack_matrix(matrix):
                        data = struct.pack('<h', x)
                        file.write(data)
                    print()

            elif i.key == pygame.K_l:
                name = labyrinth_name()
                with open((name + ".rara"), "rb") as file:
                    signa = file.read(4)
                    if signa == b'rara':
                        w = struct.unpack('<b', file.read(1))[0]
                        h = struct.unpack('<b', file.read(1))[0]
                        startf = (struct.unpack('<b', file.read(1))[0], struct.unpack('<b', file.read(1))[0])
                        finishf = (struct.unpack('<b', file.read(1))[0], struct.unpack('<b', file.read(1))[0])
                        f = 1
                        matrixf = [[] for ii in range(h)]
                        index = 0
                        while f:
                            try:
                                b = struct.unpack('<h', file.read(2))[0]
                                b = str(bin(b))[3:]
                                while b != '':
                                    matrixf[index // h].append(int(b[-1]))
                                    b = b[:-1]
                                    index += 1
                            except:
                                f = 0

                        height_windowf = formula((h + 1) // 2)
                        width_windowf = formula((w + 1) // 2)
                        text3 = font.render("ЛКМ - след.лабиринт", True, (255, 255, 255))
                        text2 = font.render("L - загрузить лабиринт", True, (255, 255, 255))
                        text1 = font.render("S - сохранить лабиринт", True, (255, 255, 255))
                        window.blit(text3, (10, height_windowf))
                        window.blit(text2, (10, height_windowf + 20))
                        window.blit(text1, (10, height_windowf + 40))
                        pygame.display.update()


                        window.fill((0, 0, 0))
                        window = pygame.display.set_mode((width_windowf, height_windowf + 70))
                        pygame.draw.rect(window, (0, 0, 0), (0, height_windowf - 70, width_windowf, 70))
                        draw_labyrinth(matrixf, startf, finishf, width_line, width_walls, color_way,
                                       color_wall,
                                       border, color_start, color_finish)
                        pygame.display.update()

x1




