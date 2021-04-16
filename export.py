import pygame_gui  # pygame-gui
import pygame  # pygame
import subprocess
import matplotlib
import os  # os
from fpdf import FPDF  # PyFPDF
import fitz  # PyMuPDF
import shutil
from math import floor

#  TODO: место сохранения 5
#  TODO: если что - новый файл
#  TODO: автоперенос и автоформат (обсудить)
#  TODO: динамический интерфейс
#  TODO: интерфейс 7

# vars
save_name = 'задания'  # имя сохранения, по умолчанию - 'задания'
widgets_x = 415
curr_img = 0
scroll_counter = 0
scrolls_to_change = 5
PDF_printer = r'/PDFPrinter/PDFPrinter.exe'
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = r'''\usepackage{amsmath}
\usepackage[russian]{babel}'''
img_w = {}
default_font_size = 15
default_dpi = 300


# A4  - 595 x 845


def count_running(a):
    res = 0
    for i in a:
        if i.poll() == None:
            res += 1
    return res


def sign(a):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0


def create_latex_pdf(num=0):
    if num == 0:
        pdf = FPDF()  # создаем временный pdf с помощью PyFPDF
        pdf.add_page()  # добавляем страницу
        pdf.image(f'temp_files/latex.png', x=10, y=8, w=img_w[''])  # вставляем картинку
        pdf.output("temp_files/latex.pdf")  # сохраняем
    else:
        pdf = FPDF()  # создаем временный pdf с помощью PyFPDF
        pdf.set_auto_page_break(False)
        pdf.set_font('Arial', size=15)
        for i in range(num):
            pdf.add_page()  # добавляем страницу
            rel_w = img_w[str(i + 1)][0] / 210
            rel_h = img_w[str(i + 1)][1] / 297
            if rel_w >= 1 and rel_w >= rel_h:
                pdf.image(f'temp_files/latex{str(i + 1)}.png', x=0, y=0, w=210)
            elif rel_h >= 1 and rel_h >= rel_w:
                pdf.image(f'temp_files/latex{str(i + 1)}.png', x=0, y=0, h=297)
            else:
                pdf.image(f'temp_files/latex{str(i + 1)}.png', x=0, y=0, w=img_w[str(i + 1)][0])
            # str(pdf.page_no())
            pdf.set_y(-10)
            pdf.cell(0, 0, str(pdf.page_no()), 0, 0, 'C')
        pdf.output("temp_files/latex.pdf")  # сохраняем


def create_latex_a4(num=0):
    if num == 0:
        pdffile = 'temp_files/latex.pdf'  # чтобы сделать png размера A4
        doc = fitz.open(pdffile)
        page = doc.loadPage(0)
        pix = page.getPixmap()
        pix.writePNG('temp_files/latex_A4.png')
        doc.close()
    else:
        pdffile = 'temp_files/latex.pdf'  # чтобы сделать png размера A4
        doc = fitz.open(pdffile)
        for i in range(num):
            page = doc.loadPage(i)
            pix = page.getPixmap()
            pix.writePNG(f'temp_files/latex_A4{str(i + 1)}.png')
        doc.close()


def export(latex_list, font_size=15, dpi=default_dpi):
    global widgets_x, save_name, curr_img, scroll_counter, scrolls_to_change
    if isinstance(latex_list, str):
        latex_list = [latex_list]
    pages_num = len(latex_list)

    pygame.init()  # запускаем pygame
    pygame.font.init()
    manager = pygame_gui.UIManager((600, 560), 'theme.json')
    info_object = pygame.display.Info()  # информация о экране
    pygame.display.set_caption('экспорт')
    screen = pygame.display.set_mode((600, 560))  # окно
    screen_img = pygame.image.load("files/ground.jpg")
    screen.blit(screen_img, (0, 0))
    f1 = pygame.font.SysFont('Calibri', 36)
    f2 = pygame.font.SysFont('Calibri', 18)
    manager.draw_ui(screen)
    pygame.display.update()
    clock = pygame.time.Clock()

    latex_list2 = latex_list.copy()
    name = 1
    processes = []
    while len(latex_list2):  # пока остались картинки для рендера
        if count_running(processes) < 10:  # если активно меньше 10 процессов
            processes.append(subprocess.Popen(  # запуск моего модуля из командной строки (см модуль latex_render.py)
                [r'C:\Users\ПК\Desktop\проги\проект9.2\fout\venv\Scripts\python.exe',
                 r'C:/Users/ПК/Desktop/проги/проект9.2/fout/latex_render.py',
                 r'--name=' + str(name), r'--fs=' + str(default_font_size),
                 r'--dpi=' + str(default_dpi), r'--ls=' + latex_list2.pop(0)]))
            name += 1  # меняем имя для следующей картинки
        screen.blit(screen_img, (0, 0))  # счетчик страниц и события
        text1 = f1.render(f'Страниц готово:{str(len(processes) - count_running(processes))}/{str(pages_num)}',
                          True, (0, 0, 0))
        text1_rect = text1.get_rect(center=(300, 280))
        screen.blit(text1, text1_rect)
        time_delta = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    while count_running(processes):  # пока не закончился рендер
        screen.blit(screen_img, (0, 0))  # счетчик страниц и события
        text1 = f1.render(f'Страниц готово:{str(len(processes) - count_running(processes))}/{str(pages_num)}',
                          True, (0, 0, 0))
        text1_rect = text1.get_rect(center=(300, 280))
        screen.blit(text1, text1_rect)
        time_delta = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    for i in os.listdir(os.getcwd() + '/temp_files'):
        if i[0] == 'd' and i[1] == 'i' and i[2] == 'm':
            f = open('temp_files/' + i, 'r')
            dim = f.read().split()
            f.close()
            img_w[i[3:-4]] = (int(dim[0]) / dpi * 72, int(dim[1]) / dpi * 72)
    create_latex_pdf(pages_num)
    create_latex_a4(pages_num)

    def name_upd():  # функция обновления текстового поля
        global save_name
        """ Функция считывает новое имя сохранения из текстового поля и,
            если оно изменилось, заново активирует кнопки.
            Функция меняет имя сохранения"""
        s = name_textbox.get_text()
        if save_name != s and s != '':
            save_name = s
            save_png_button.enable()
            save_pdf_button.enable()
            open_png_button.enable()
            open_pdf_button.enable()

    def save_png(name, num=0):  # сохранение в png
        """Функция принимает имя для сохранения
            Функция копирует временный .png файл и переименовывает.
            Также меняет цвет кнопки сохранения в png на более светлый """
        if num == 0:
            try:
                os.remove(os.getcwd() + f'/{name}.png')
            except FileNotFoundError:
                pass
            shutil.copy(os.getcwd() + '/temp_files/latex1.png', os.getcwd() + f'/{name}.png')
        else:
            for i in range(num):
                try:
                    os.remove(os.getcwd() + f'/{name + str(i + 1)}.png')
                except FileNotFoundError:
                    pass
                shutil.copy(os.getcwd() + f'/temp_files/latex{str(i + 1)}.png',
                            os.getcwd() + f'/{name + str(i + 1)}.png')
        save_png_button.disable()

    def open_png(name, num=0):
        if num == 0:
            try:
                os.remove(os.getcwd() + f'/{name}.png')
            except FileNotFoundError:
                pass
            shutil.copy(os.getcwd() + '/temp_files/latex1.png', os.getcwd() + f'/{name}.png')
            os.system(os.getcwd() + f'\\{name}.png')
        else:
            for i in range(num):
                try:
                    os.remove(os.getcwd() + f'/{name + str(i + 1)}.png')
                except FileNotFoundError:
                    pass
                shutil.copy(os.getcwd() + '/temp_files/latex1.png', os.getcwd() + f'/{name}.png')
                os.system(os.getcwd() + f'\\{name}1.png')
        save_png_button.disable()
        open_png_button.disable()

    def save_pdf(name):  # сохранение в pdf
        """Функция принимает имя для сохранения
            Функция копирует временный .pdf файл и переименовывает.
            Также меняет цвет кнопки сохранения в pdf на более светлый"""
        try:
            os.remove(os.getcwd() + f'/{name}.pdf')
        except FileNotFoundError:
            pass
        shutil.copy(os.getcwd() + '/temp_files/latex.pdf', os.getcwd() + f'/{name}.pdf')
        save_pdf_button.disable()

    def open_pdf(name):
        try:
            os.remove(os.getcwd() + f'/{name}.pdf')
        except FileNotFoundError:
            pass
        shutil.copy(os.getcwd() + '/temp_files/latex.pdf', os.getcwd() + f'/{name}.pdf')
        save_pdf_button.disable()
        open_pdf_button.disable()
        os.system(os.getcwd() + f'/{name}.pdf')

    def printer():
        os.popen(os.getcwd() + PDF_printer + ' ' + os.getcwd() + '/temp_files/latex.pdf')

    def page_upd(pos):
        global curr_img
        curr_img = pos
        if curr_img < 0:
            curr_img = 0
        if curr_img > pages_num - 1:
            curr_img = pages_num - 1
        screen.blit(screen_img, (0, 0))
        screen.blit(latex[curr_img], lr[curr_img])
        text2 = f2.render(f'страница {str(curr_img + 1)}/{pages_num}', True, (0, 0, 0))
        screen.blit(text2, (30, 535))
        pages_scrollbar.scroll_position = curr_img / pages_num * (
            pages_scrollbar.scrollable_height)
        pages_scrollbar.rebuild()

    latex = [pygame.image.load(f'temp_files/latex_A4{str(i + 1)}.png') for i in range(pages_num)]
    for i in range(pages_num):
        latex[i] = pygame.transform.scale(latex[i], (370, int(370 * 2 ** 0.5)))  # меняем размер
    lr = [latex[i].get_rect(topleft=(10, 10)) for i in range(pages_num)]  # прямоугольник картинки
    screen.blit(screen_img, (0, 0))

    save_png_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 10), (170, 30)),
                                                   text='сохранить в png', manager=manager)
    open_png_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 50), (170, 30)),
                                                   text='в png и открыть', manager=manager)
    save_pdf_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 90), (170, 30)),
                                                   text='сохранить в pdf', manager=manager)
    open_pdf_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 130), (170, 30)),
                                                   text='в pdf и открыть', manager=manager)
    print_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 170), (170, 30)),
                                                text='печать', manager=manager)
    name_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((widgets_x, 230), (170, 20)),
                                                       manager=manager)

    pages_scrollbar = pygame_gui.elements.UIVerticalScrollBar(
        relative_rect=pygame.Rect((380, 10), (20, int(370 * 2 ** 0.5))), visible_percentage=1 / pages_num,
        manager=manager)
    page_upd(0)
    name_textbox.set_text(save_name)
    name_label = pygame.font.SysFont('Calibri', 14)
    name_label = name_label.render('Имя сохранения:', True, (0, 0, 0))
    screen.blit(name_label, (widgets_x + 7, 213))

    is_running = True
    while is_running:  # цикл событий
        time_delta = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                for tf in os.listdir(os.getcwd() + '/temp_files'):
                    os.remove(os.getcwd() + '/temp_files/' + tf)
                break

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == save_png_button:
                        if pages_num > 1:
                            save_png(save_name, pages_num)
                        else:
                            save_png(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == open_png_button:
                        if pages_num > 1:
                            open_png(save_name, pages_num)
                        else:
                            open_png(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == save_pdf_button:
                        save_pdf(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == open_pdf_button:
                        open_pdf(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == print_button:
                        printer()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element == name_textbox:
                        name_upd()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == 'vertical_scroll_bar.#bottom_button':
                        page_upd(curr_img + 1)

            ifevent.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                scroll_counter -= 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                scroll_counter += 1

            manager.process_events(event)

        if not is_running:
            break

        if abs(scroll_counter) >= scrolls_to_change:
            page_upd(curr_img + sign(scroll_counter))
            scroll_counter = 0

        if pages_scrollbar.check_has_moved_recently():
            page_upd(floor(
                pages_num * pages_scrollbar.scroll_position / (
                    pages_scrollbar.scrollable_height)))
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


# 06.04.21 код Зверева Алексея был изменен, теперь код ниже не основан на его коде
# ------------------- Автор участка кода ниже - Кудряшов Илья (код основан на коде Зверева Алексея) -------------------
def text_to_pdf(text, font):  # Функция для самой простой отрисовки текста на pdf-документе средствами pygame
    pages = text.split('{nextpage}')  # {nextpage} mean... well... next page
    num = len(pages)
    for i, page in enumerate(pages):  # Разбиваем текст на страницы и создаём для каждой изображение
        lines = page.split('\n')
        imgs = []
        size = [0, 0]
        poses = []
        for line in lines:  # разбиваем текст на строки, т.к. pygame этого делать не может
            imgs.append(font.render(line, True, (0, 0, 0)))
            poses.append(size[1])
            size = [max(size[0], imgs[-1].get_width()), size[1] + imgs[-1].get_height() + 3]
        pre_save = pygame.Surface(size)
        pre_save.fill([255, 255, 255])
        for j, img in enumerate(imgs):
            pre_save.blit(img, [0, poses[j]])
        pygame.image.save(pre_save, f'temp_files/latex{str(i + 1)}.png')
    if num == 0:
        pdf = FPDF()  # создаем временный pdf с помощью PyFPDF
        pdf.add_page()  # добавляем страницу
        pdf.image(f'temp_files/latex.png', x=10, y=8)  # , w=img_w[''])  # вставляем картинку
        pdf.output("temp_files/latex.pdf")  # сохраняем
    else:
        pdf = FPDF()  # создаем временный pdf с помощью PyFPDF
        for i in range(num):
            pdf.add_page()  # добавляем страницу
            pdf.image(f'temp_files/latex{str(i + 1)}.png', x=10, y=8)  # , w=img_w[str(i + 1)])
        pdf.output("temp_files/latex.pdf")  # сохраняем


def export_alternative(latex_list, font_size=15, dpi=default_dpi):
    global widgets_x, save_name, curr_img, scroll_counter, scrolls_to_change
    pages_num = len(latex_list.split('{nextpage}'))
    pygame.init()  # запускаем pygame
    pygame.font.init()
    manager = pygame_gui.UIManager((600, 560), 'Resource/main/descr1.json')
    info_object = pygame.display.Info()  # информация о экране
    screen = pygame.display.set_mode((600, 560))  # окно
    screen_img = pygame.image.load("Resource/main/ground.jpg")
    screen.blit(screen_img, (0, 0))
    f1 = pygame.font.SysFont('Calibri', 36)
    f2 = pygame.font.SysFont('Calibri', 18)
    text1 = f1.render('Ждите...', True, (0, 0, 0))
    screen.blit(text1, (265, 255))
    manager.draw_ui(screen)
    pygame.display.update()

    fnt = pygame.font.SysFont('Calibri', font_size)
    text_to_pdf(latex_list, fnt)
    create_latex_a4(pages_num)  # Латех - ложь! Эта функция просто преобразует pdf-файл в нужный формат.

    def name_upd():  # функция обновления текстового поля
        global save_name
        """ Функция считывает новое имя сохранения из текстового поля и,
            если оно изменилось, заново активирует кнопки.
            Функция меняет имя сохранения"""
        s = name_textbox.get_text()
        if save_name != s and s != '':
            save_name = s
            save_png_button.enable()
            save_pdf_button.enable()
            open_png_button.enable()
            open_pdf_button.enable()

    def save_png(name, num=0):  # сохранение в png
        """Функция принимает имя для сохранения
            Функция копирует временный .png файл и переименовывает.
            Также меняет цвет кнопки сохранения в png на более светлый """
        if num == 0:
            try:
                os.remove(os.getcwd() + f'/{name}.png')
            except FileNotFoundError:
                pass
            shutil.copy(os.getcwd() + '/temp_files/latex1.png', os.getcwd() + f'/{name}.png')
        else:
            for i in range(num):
                try:
                    os.remove(os.getcwd() + f'/{name + str(i + 1)}.png')
                except FileNotFoundError:
                    pass
                shutil.copy(os.getcwd() + f'/temp_files/latex{str(i + 1)}.png',
                            os.getcwd() + f'/{name + str(i + 1)}.png')
        save_png_button.disable()

    def open_png(name, num=0):
        if num == 0:
            try:
                os.remove(os.getcwd() + f'/{name}.png')
            except FileNotFoundError:
                pass
            shutil.copy(os.getcwd() + '/temp_files/latex1.png', os.getcwd() + f'/{name}.png')
            os.system(os.getcwd() + f'\\{name}.png')
        else:
            for i in range(num):
                try:
                    os.remove(os.getcwd() + f'/{name + str(i + 1)}.png')
                except FileNotFoundError:
                    pass
                shutil.copy(os.getcwd() + '/temp_files/latex1.png', os.getcwd() + f'/{name}.png')
                os.system(os.getcwd() + f'\\{name}1.png')
        save_png_button.disable()
        open_png_button.disable()

    def save_pdf(name):  # сохранение в pdf
        """Функция принимает имя для сохранения
            Функция копирует временный .pdf файл и переименовывает.
            Также меняет цвет кнопки сохранения в pdf на более светлый"""
        try:
            os.remove(os.getcwd() + f'/{name}.pdf')
        except FileNotFoundError:
            pass
        shutil.copy(os.getcwd() + '/temp_files/latex.pdf', os.getcwd() + f'/{name}.pdf')
        save_pdf_button.disable()

    def open_pdf(name):
        try:
            os.remove(os.getcwd() + f'/{name}.pdf')
        except FileNotFoundError:
            pass
        shutil.copy(os.getcwd() + '/temp_files/latex.pdf', os.getcwd() + f'/{name}.pdf')
        save_pdf_button.disable()
        open_pdf_button.disable()
        os.system(os.getcwd() + f'/{name}.pdf')

    def printer():
        os.popen(os.getcwd() + PDF_printer + ' ' + os.getcwd() + '/temp_files/latex.pdf')

    def page_upd(pos):
        global curr_img
        curr_img = pos
        if curr_img < 0:
            curr_img = 0
        if curr_img > pages_num - 1:
            curr_img = pages_num - 1
        screen.blit(screen_img, (0, 0))
        screen.blit(latex[curr_img], lr[curr_img])
        text2 = f2.render(f'страница {str(curr_img + 1)}/{pages_num}', True, (0, 0, 0))
        screen.blit(text2, (30, 535))
        pages_scrollbar.scroll_position = curr_img / pages_num * (
            pages_scrollbar.scrollable_height)
        pages_scrollbar.rebuild()

    #  TODO: норм качество
    latex = [pygame.image.load(f'temp_files/latex_A4{str(i + 1)}.png') for i in range(pages_num)]
    for i in range(pages_num):
        latex[i] = pygame.transform.scale(latex[i], (370, int(370 * 2 ** 0.5)))  # меняем размер
    lr = [latex[i].get_rect(topleft=(10, 10)) for i in range(pages_num)]  # прямоугольник картинки
    screen.blit(screen_img, (0, 0))

    save_png_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 10), (170, 30)),
                                                   text='сохранить в png', manager=manager)
    open_png_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 50), (170, 30)),
                                                   text='в png и открыть', manager=manager)
    save_pdf_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 90), (170, 30)),
                                                   text='сохранить в pdf', manager=manager)
    open_pdf_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 130), (170, 30)),
                                                   text='в pdf и открыть', manager=manager)
    print_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((widgets_x, 170), (170, 30)),
                                                text='печать', manager=manager)
    name_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((widgets_x, 230), (170, 20)),
                                                       manager=manager)

    pages_scrollbar = pygame_gui.elements.UIVerticalScrollBar(
        relative_rect=pygame.Rect((380, 10), (20, int(370 * 2 ** 0.5))), visible_percentage=1 / pages_num,
        manager=manager)
    page_upd(0)
    name_textbox.set_text(save_name)
    name_label = pygame.font.SysFont('Calibri', 14)
    name_label = name_label.render('Имя сохранения:', True, (0, 0, 0))
    screen.blit(name_label, (widgets_x + 7, 213))
    clock = pygame.time.Clock()

    is_running = True
    while is_running:  # цикл событий
        time_delta = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                for tf in os.listdir(os.getcwd() + '/temp_files'):
                    os.remove(os.getcwd() + '/temp_files/' + tf)
                break

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == save_png_button:
                        if pages_num > 1:
                            save_png(save_name, pages_num)
                        else:
                            save_png(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == open_png_button:
                        if pages_num > 1:
                            open_png(save_name, pages_num)
                        else:
                            open_png(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == save_pdf_button:
                        save_pdf(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == open_pdf_button:
                        open_pdf(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == print_button:
                        printer()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element == name_textbox:
                        name_upd()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == 'vertical_scroll_bar.#bottom_button':
                        page_upd(curr_img + 1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                scroll_counter -= 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                scroll_counter += 1

            manager.process_events(event)

        if not is_running:
            break

        if abs(scroll_counter) >= scrolls_to_change:
            page_upd(curr_img + sign(scroll_counter))
            scroll_counter = 0

        if pages_scrollbar.check_has_moved_recently():
            page_upd(floor(
                pages_num * pages_scrollbar.scroll_position / (
                    pages_scrollbar.scrollable_height)))
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


# ------------------- Автор участка кода выше - Кудряшов Илья (код основан на коде Зверева Алексея) --------------------


if __name__ == '__main__':
    ls = ['$x^2$','$x^3$','$x^4$']
    export(ls, dpi=default_dpi)
