import pygame
from pygame.locals import *
import pygame_gui
import time

pygame.init()


def imload(name, pos=[0, 0]):
    img = pygame.image.load('Images/' + name)
    img.set_colorkey(img.get_at(pos))
    return img


def border(string):
    return string[string.find('(') + 1: string.rfind(')')]


"""
Извлекает значение внутри скобок в строке
string - исходная строка (обязана содержать хотя бы одну открывающую и закрывающую скобку в нужном порядке)
"""


def string_to_number(string):
    if len(string) == 0:
        return '0'
    answ = ''
    if string[0] == '-':
        answ = '-'
        string = string[1:]
    was_dot = False
    for i in range(0, len(string)):
        if string[i] in '.,' and i != 0 and not was_dot:
            was_dot = True
            answ = answ + '.'
        if string[i] in '1234567890':
            answ = answ + string[i]
    if len(answ) == 0:
        return '0'
    while answ[0] == 0:
        answ = answ[1:]
    if answ[0] == '.':
        while answ[1] == 0:
            answ = '-' + answ[2:]
    if answ[0] == '-':
        while answ[1] == 0:
            answ = '-' + answ[2:]
        if answ[1] == '.':
            while answ[1] == 0:
                answ = '-' + answ[2:]
    return answ


class UIElement:
    typ = 'None'
    name = ''
    ID = ''
    default = ''
    options = []

    def __init__(self, typ, name, options=[], default='', ID=''):
        self.typ = typ
        self.name = name
        self.default = default
        self.options = options.copy()
        self.ID = ID

    def get_gui(self, rect, manager):  # Возвращает объект GUI
        shift = 2
        if self.typ == 'chek':
            description = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((rect[0], rect[1] + 2), (rect[2] - rect[3] - 10, rect[3] - 2 * shift)),
                text=self.name,
                manager=manager,
                visible=True)
        else:
            description = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((rect[0], rect[1] + 2), (rect[2] // 2 - 30, rect[3] - 2 * shift)),
                text=self.name,
                manager=manager,
                visible=True)
        if self.typ == 'text':
            answ = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
                relative_rect=pygame.Rect((rect[0] + rect[2] // 2 - 20, rect[1]), (rect[2] // 2 + 20, rect[3])),
                manager=manager)
            answ.set_text(self.default)
            return answ
        if self.typ == 'numb':
            answ = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
                relative_rect=pygame.Rect((rect[0] + rect[2] // 2 - 20, rect[1]), (rect[2] // 2 + 20, rect[3])),
                manager=manager)
            answ.set_text(self.default)
            return answ
        if self.typ == 'list':
            return pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=self.options.copy(),
                                                                        starting_option=self.default,
                                                                        relative_rect=pygame.Rect(
                                                                            (rect[0] + rect[2] // 2 - 20, rect[1]),
                                                                            (rect[2] // 2 + 20, rect[3])),
                                                                        manager=manager)
        if self.typ == 'radi':
            return pygame_gui.elements.UISelectionList(
                relative_rect=pygame.Rect((rect[0] + rect[2] // 2 - 20, rect[1]), (rect[2] // 2 + 20, rect[3])),
                item_list=self.options.copy(),
                manager=manager,
                allow_double_clicks=False,
                allow_multi_select=False)
        if self.typ == 'chek':  # Да, я знаю, что здесь ошибка и правильно с точки зрения грамматики писать "check", но я специально сократил слово до 4 букв
            return pygame_gui.elements.UISelectionList(
                relative_rect=pygame.Rect((rect[0] + rect[2] - rect[3], rect[1]), (rect[3], rect[3])),
                item_list=[' '],
                manager=manager,
                allow_double_clicks=False,
                allow_multi_select=True)


"""
Класс для временного хранения результатов расшифровки входной строки программы.
"""


def decode_uis(string):
    answ = []
    arr = string.split(';')
    for com in arr:
        s = border(com).split(',')
        for i in range(len(s)):
            if s[i][0] == ' ':
                s[i] = s[i][1:]
        if com.replace(' ', '')[:4] == 'text':
            answ.append(UIElement('text', name=s[0], default=s[2], ID=s[1]))
        if com.replace(' ', '')[:4] == 'numb':
            answ.append(UIElement('numb', name=s[0], default=s[2], ID=s[1]))
        if com.replace(' ', '')[:4] == 'list':
            answ.append(UIElement('list', name=s[0], default=s[2], ID=s[1], options=s[3:]))
        if com.replace(' ', '')[:4] == 'radi':
            answ.append(UIElement('radi', name=s[0], ID=s[1], options=s[2:]))
        if com.replace(' ', '')[:4] == 'chek':
            answ.append(UIElement('chek', name=s[0], ID=s[1]))
    return answ


"""
Функция для расшифровки входной строки (ввода) программы
"""


class Drawer:
    def __init__(self, params='', description='Нет описания генератора :('):
        self.description = description.replace('\n', '<br>')
        self.UIs = decode_uis(params)
        self.scr = pygame.display.set_mode([1100, 600])
        pygame.display.set_caption('GRIT-Z')  # Generator of Randomized Instances of Tasks - Zero edition
        self.reset(params)
        self.tm = time.monotonic()
        self.bg = pygame.image.load('Images/ground.jpg')
        self.flag = imload('flag.bmp')
        self.cross = imload('cross.bmp')

    def reset(self, params):  # Пересоздаёт меню с другими настройками (ввод)
        self.manager = pygame_gui.UIManager([1100, 600], 'Styles/style.json')
        self.generate_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 20), (800 - 30 - 600, 50)),
                                                            text='Generate',
                                                            manager=self.manager)
        pygame_gui.elements.ui_text_box.UITextBox(relative_rect=pygame.Rect((800, 20), (270, 560)),
                                                  html_text=self.description,
                                                  manager=self.manager)
        self.uis = decode_uis(params)
        self.guis = []
        curent_position = 20
        self.rects = []
        for i, ui in enumerate(self.uis):
            if ui.typ == 'radi':
                height = 22 * (len(ui.options))
            else:
                height = 26
            self.guis.append(ui.get_gui([20, curent_position, 250 + 300, height],
                                        self.manager))
            self.rects.append([20, curent_position, 250 + 300, height])
            curent_position += height + 3

    def get_values(self):  # Возвращает массив значений элементов интерфейса
        answ = []
        ids = [x.ID for x in self.uis]
        for ui in self.guis:
            try:
                answ.append(ui.selected_option)
            except:
                try:
                    answ.append(ui.get_text())
                except:
                    try:
                        answ.append(str(ui.get_single_selection()))
                    except:
                        answ.append(str(len(ui.get_multi_selection())))
        use_brackets = False
        if use_brackets:
            return '{' + ', '.join(
                ['\'' + str(ids[i]) + '\' : \'' + str(answ[i]) + '\'' for i in range(len(ids))]) + '}'
        return ', '.join([str(ids[i]) + ' : ' + str(answ[i]) for i in range(len(ids))])

    def operate_events(self):  # Обрабатывает события пользователя.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'stop'
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.generate_button:
                        return self.get_values()
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    i = self.guis.index(event.ui_element)
                    if self.uis[i].typ == 'numb':
                        self.guis[i].set_text(string_to_number(self.guis[i].get_text()))
            self.manager.process_events(event)

    def tick(self):  # Функция для обновления. Должна вызываться каждый проход основного цикла программы.
        TM = time.monotonic()
        delta = TM - self.tm
        self.tm = TM
        res = self.operate_events()
        self.manager.update(delta)
        self.scr.blit(self.bg, [0, 0])
        self.manager.draw_ui(self.scr)
        for i in range(len(self.uis)):
            if self.uis[i].typ == 'chek':
                img = self.cross
                if len(self.guis[i].get_multi_selection()):
                    img = self.flag
                rect = self.rects[i]
                shift = 3
                pos_x = rect[0] + rect[2] - rect[3] + shift
                pos_y = rect[1] + shift
                self.scr.blit(pygame.transform.scale(img, [rect[3] - 2 * shift] * 2), [pos_x, pos_y])
        pygame.display.update()
        return res


"""
Основной класс программы
"""


def get_interface_input(params='', description='Нет описания генератора :('):
    log = open('Logs/Interface_log.txt', 'w')
    print('params -', params, '\ndescription -', description, '\n', file=log)
    log.close()
    drw = Drawer(params, description=description)
    kg = True  # Условие основного цикла программы
    while kg:  # ОЦП (Основной Цикл Программы)
        res = drw.tick()  # Обновление интерфейса и приём команд пользователя. Для пересоздания интерфейса используется функция reset("новый_ввод")
        # Обработка вывода интерфейса
        if res == 'stop':
            kg = False
            pygame.quit()
            log = open('Logs/Interface_log.txt', 'r')
            text = log.read()
            log.close()
            log = open('Logs/Interface_log.txt', 'w')
            print(text, file=log)
            print('Program closed by user. None returned.', file=log)
            log.close()
            return None
            break
        elif res is not None:
            pygame.quit()
            log = open('Logs/Interface_log.txt', 'r')
            text = log.read()
            log.close()
            log = open('Logs/Interface_log.txt', 'w')
            print(text, file=log)
            print('Generate event got. Params -', res, file=log)
            log.close()
            return res
