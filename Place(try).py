import pygame
import pygame_gui
import os


def names(subj, theme):
    global gens1
    gens1 = []
    for i in gens:
        demo_file = open(r"Subjects/" + subj + "/" + str(theme) + "/" + i, encoding='utf-8')
        title = demo_file.readline()
        title = title.split('# ')[1]
        title = title.split('\n')[0]
        gens1.append(title)
        demo_file.close()


def load_gen(subj, theme, gen):  # запуск генератора
    path = os.getcwd()
    print(path)
    if gen != "" and theme != "" and subj != "":
        # os.startfile(path + "/Subjects/" + subj + "/" + theme + "/" + gen)
        os.system('python "' + path + "\\Subjects\\" + subj + "\\" + theme + "\\" + gen + '"')


def draw(subj, theme, gen):  # переотрисовка окна
    global themes, texts
    if len(themes) > 0:
        # print(theme)
        demo_file = open(r"Subjects/" + subj + "/" + str(theme) + "/" + gen, encoding='utf-8')
        text = ""
        for i in demo_file:
            if "# &" in i:
                texts.kill()
                story = i.split("# &")[1]
                story = story.split('\n')[0]
                text += story
        texts = pygame_gui.elements.UITextBox(html_text=text, relative_rect=pygame.Rect(250, 50, 520, 350),
                                              manager=manager)
        demo_file.close()

    else:
        text = "Заданий нет"
        texts.kill()
        texts = pygame_gui.elements.UITextBox(html_text=text,
                                              relative_rect=pygame.Rect(250, 50, 520, 350), manager=manager)


pygame.init()
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

screen = pygame.image.load("resources/ground.jpg")
manager = pygame_gui.UIManager((800, 600), 'resources/descr1.json')
clock = pygame.time.Clock()

directory = 'Subjects'
files = os.listdir(directory)  # тут храним предметы
if len(files) == 0:
    subj = ""
else:
    subj = files[0]

themes = os.listdir("Subjects/" + subj)  # тут храним темы предмета
if len(themes) == 0:
    theme = ""
else:
    theme = themes[0]

gens = os.listdir("Subjects/" + subj + "/" + theme)  # тут храним генераторы темы
if len(gens) == 0:
    gen = ""
else:
    gen = gens[0]

# кнопка запуска генератора
gen_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 450), (100, 50)),
                                          text='Generate',
                                          manager=manager)
# текстовое поле
texts = pygame_gui.elements.UITextBox(html_text="Ничего нет", relative_rect=pygame.Rect(250, 50, 520, 350),
                                      manager=manager)
# список предметов
subj_drop = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(10, 50, 170, 100), item_list=files,
                                                manager=manager, allow_double_clicks=False, allow_multi_select=False)
# список тем
theme_drop = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(10, 200, 220, 150), item_list=themes,
                                                 manager=manager, allow_double_clicks=False, allow_multi_select=False)
# список генераторов
gens1 = []
names(subj, theme)
gen_drop = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(10, 400, 220, 100), item_list=gens1,
                                               manager=manager, allow_double_clicks=False, allow_multi_select=False)

is_running = True
while is_running:  # основной цикл
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:  # события
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gen_button:
                    if len(themes) > 0:
                        load_gen(subj, theme, gen)

            if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == subj_drop:
                    theme_drop.kill()
                    themes = os.listdir("Subjects/" + event.text)
                    theme_drop = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(10, 200, 220, 150),
                                                                     item_list=themes,
                                                                     manager=manager, allow_double_clicks=False,
                                                                     allow_multi_select=False)
                    if len(themes) == 0:
                        theme = ""
                    else:
                        theme = themes[0]
                    subj = event.text
                    gen_drop.kill()
                    gens = os.listdir("Subjects/" + subj + "/" + theme)
                    gens1 = []
                    if len(gens) > 0:
                        names(subj, theme)
                    gen_drop = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(10, 400, 220, 100),
                                                                   item_list=gens1,
                                                                   manager=manager, allow_double_clicks=False,
                                                                   allow_multi_select=False)
                    if len(gens) == 0:
                        gen = ""
                    else:
                        gen = gens[0]
                    print("Selected option:", event.text)

                if event.ui_element == theme_drop:
                    gen_drop.kill()
                    theme = event.text
                    gens = os.listdir("Subjects/" + subj + "/" + event.text)
                    names(subj, theme)
                    gen_drop = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(10, 400, 220, 100),
                                                                   item_list=gens1,
                                                                   manager=manager, allow_double_clicks=False,
                                                                   allow_multi_select=False)
                    if len(gens) == 0:
                        gen = ""
                    else:
                        gen = gens[0]
                    theme = event.text
                    print("Selected option:", event.text)

                if event.ui_element == gen_drop:
                    gen = event.text
                    gen = gens[gens1.index(gen)]
                    print("Selected option:", event.text)

        if gen != "" and theme != "" and subj != "":
            draw(subj, theme, gen)
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(screen, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
