import pygame
import pygame_gui
import os

pygame.init()
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

screen = pygame.image.load("files/ground.jpg")
# screen = pygame.Surface((800, 600))
# screen.fill([59, 70, 115])

manager = pygame_gui.UIManager((800, 600), 'files/descr1.json')
# кнопки

gen_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 450), (100, 50)),
                                          text='Generate',
                                          manager=manager)
# меню предметов
directory = 'Subjects'
files = os.listdir(directory)
subj = files[0]
themes = os.listdir("Subjects/" + subj)
subj_drop = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=files,
                                                                 starting_option=files[0],
                                                                 relative_rect=pygame.Rect(0, 50, 170, 40),
                                                                 manager=manager)
theme_drop = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=themes,
                                                                  starting_option=themes[0],
                                                                  relative_rect=pygame.Rect(0, 200, 170, 40),
                                                                  manager=manager)
texts = pygame_gui.elements.UITextBox(html_text="Ничего нет", relative_rect=pygame.Rect(200, 50, 550, 350),
                                      manager=manager)
# answ = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect(200, 200, 200, 200), manager=manager, text_image_rect=pygame.Rect(200,200,200,200))
# answ.set_text("hi")
clock = pygame.time.Clock()
is_running = True
theme = themes[0]


def load_gen(subj, theme):  # запуск генератора
    os.startfile("C:/Users/Xiaomi/Documents/school/ProjGens/Subjects/" + subj + "/" + theme)


def draw(subj, theme):  # переотрисовка окна
    global themes, texts
    # pygame.draw.rect(screen, (0, 0, 0), (150, 100, 500, 400), 4)
    y = 120
    if len(themes) > 0:
        # print(theme)
        demo_file = open(r"Subjects/" + subj + "/" + str(theme), encoding='utf-8')
        text = ""
        for i in demo_file:
            if "# &" in i:
                texts.kill()
                story = i.split("# &")[1]
                story = story.split('\n')[0]
                text += story
        texts = pygame_gui.elements.UITextBox(html_text=text, relative_rect=pygame.Rect(200, 50, 550, 350),
                                              manager=manager)
        demo_file.close()

    else:
        text = "Заданий нет"
        texts.kill()
        texts = pygame_gui.elements.UITextBox(html_text=text,
                                              relative_rect=pygame.Rect(200, 50, 550, 350), manager=manager)


while is_running:  # основной цикл
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:  # события
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gen_button:
                    # screen.fill(pygame.Color('#FFFFFF'))
                    if len(themes) > 0:
                        load_gen(subj, theme)
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                # screen.fill(pygame.Color('#FFFFFF'))
                if event.ui_element == subj_drop:
                    theme_drop.kill()
                    themes = os.listdir("Subjects/" + event.text)
                    theme_drop = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=themes,
                                                                                      starting_option=themes[0],
                                                                                      relative_rect=pygame.Rect(0, 200,
                                                                                                                170,
                                                                                                                40),
                                                                                      manager=manager)
                    theme = themes[0]
                    subj = event.text
                    print("Selected option:", event.text)
                if event.ui_element == theme_drop:
                    theme = event.text
                    draw(subj, theme)
                    print("Selected option:", event.text)
        draw(subj, theme)
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(screen, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
