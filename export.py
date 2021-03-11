import win32api  # pywin32
import pygame_gui  # pygame-gui
import pygame  # pygame
import matplotlib.pyplot as plt  # matplotlib
import matplotlib
from PIL import Image  # pillow
import os  # os
from fpdf import FPDF  # PyFPDF
import fitz  # PyMuPDF
import shutil
from math import ceil

# consts
save_name = 'задания'  # имя сохранения, по умолчанию - 'задания'
widgets_x = 390
curr_img = 0
scroll_counter = 0
scrolls_to_change = 5
PDF_reader = os.getcwd() + '/SumatraPDF/SumatraPDF.exe'


#  TODO: динамический интерфейс 1

def sign(a):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0


def create_latex(latex_string, name=''):
    plt.figure(1, figsize=(10, 10))
    ax = plt.axes([0, 0, 1, 1])
    ax.set_axis_off()
    matplotlib.rcParams['text.usetex'] = True
    matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
    ax.text(0.5, 0.5, latex_string,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color='black')
    plt.savefig(f'temp_files/latex{name}.png')
    plt.close()


def crop_latex(name=''):
    image = Image.open(f'temp_files/latex{name}.png')  # обрезаем картинку с помощью PIL
    pix = image.load()  # массив пикселей
    x1, y1, x2, y2 = image.size[0], image.size[1], 0, 0,  # координаты краев текста
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if pix[x, y][0] < 255 or pix[x, y][1] < 255 or pix[x, y][2] < 255:
                x1 = min(x, x1)
                y1 = min(y, y1)
                x2 = max(x, x2)
                y2 = max(y, y2)
    image = image.crop((x1 - 3, y1 - 3, x2 + 3, y2 + 3))  # немного оставил запас
    image.save(f"temp_files/latex{name}.png")


def create_latex_pdf(num=0):
    if num == 0:
        pdf = FPDF()  # создаем временный pdf с помощью PyFPDF
        pdf.add_page()  # добавляем страницу
        pdf.image(f'temp_files/latex.png', x=10, y=8)  # вставляем картинку
        pdf.output("temp_files/latex.pdf")  # сохраняем
    else:
        pdf = FPDF()  # создаем временный pdf с помощью PyFPDF
        for i in range(num):
            pdf.add_page()  # добавляем страницу
            pdf.image(f'temp_files/latex{str(i + 1)}.png', x=10, y=8)
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


def export(latex_list):
    global widgets_x, save_name, curr_img, scroll_counter, scrolls_to_change
    if isinstance(latex_list, str):
        latex_list = [latex_list]
    pages_num = len(latex_list)
    """функция принимает текст LaTex'а, заключенный в доллары, и занимается выводом
            баги:  не работает с большими текстами"""
    pygame.init()  # запускаем pygame
    pygame.font.init()
    manager = pygame_gui.UIManager((570, 540), 'theme.json')
    info_object = pygame.display.Info()  # информация о экране
    screen = pygame.display.set_mode((570, 540))  # окно
    screen_img = pygame.image.load("files/ground.jpg")
    screen.blit(screen_img, (0, 0))
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render('Ждите...', True, (0, 0, 0))
    screen.blit(text1, (265, 255))
    manager.draw_ui(screen)
    pygame.display.update()

    for i in range(pages_num):
        create_latex(latex_list[i], str(i + 1))  # создание картинок с формулами
        crop_latex(str(i + 1))
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
            shutil.copy(os.getcwd() + '/temp_files/latex.png', os.getcwd() + f'/{name}.png')
        else:
            for i in range(num):
                shutil.copy(os.getcwd() + f'/temp_files/latex{str(i + 1)}.png',
                            os.getcwd() + f'/{name + str(i + 1)}.png')
        save_png_button.disable()

    def open_png(name, num=0):
        if num == 0:
            if f'{name}.png' not in os.listdir(os.getcwd()):
                shutil.copy(os.getcwd() + '/temp_files/latex1.png', os.getcwd() + f'/{name}.png')
            os.system(os.getcwd() + f'\\{name}.png')
        else:
            if f'{name}1.png' not in os.listdir(os.getcwd()):
                for i in range(num):
                    shutil.copy(os.getcwd() + '/temp_files/latex1.png', os.getcwd() + f'/{name}.png')
                os.system(os.getcwd() + f'\\{name}1.png')
        save_png_button.disable()
        open_png_button.disable()

    def save_pdf(name):  # сохранение в pdf
        """Функция принимает имя для сохранения
            Функция копирует временный .pdf файл и переименовывает.
            Также меняет цвет кнопки сохранения в pdf на более светлый"""
        shutil.copy(os.getcwd() + '/temp_files/latex.pdf', os.getcwd() + f'/{name}.pdf')
        save_pdf_button.disable()

    def open_pdf(name):
        if f'{name}.pdf' not in os.listdir(os.getcwd()):
            shutil.copy(os.getcwd() + '/temp_files/latex.pdf', os.getcwd() + f'/{name}.pdf')
        save_pdf_button.disable()
        open_pdf_button.disable()
        os.system(PDF_reader + ' ' + os.getcwd() + f'/{name}.pdf')

    #  TODO: проверить 7
    def printer():
        win32api.ShellExecute(0, 'print', os.getcwd() + 'temp_files/latex.pdf', '.', '/manualstoprint',
                              0)  # по идее так

    #  TODO: норм скроллбар  и указатель 7
    def page_upd():
        global curr_img
        if curr_img < 0:
            curr_img = 0
        if curr_img > pages_num - 1:
            curr_img = pages_num - 1
        screen.blit(latex[curr_img], lr[curr_img])

    #  TODO: норм качество 1
    latex = [pygame.image.load(f'temp_files/latex_A4{str(i + 1)}.png') for i in range(pages_num)]
    for i in range(pages_num):
        latex[i] = pygame.transform.scale(latex[i], (370, int(370 * 2 ** 0.5)))  # меняем размер
    lr = [latex[i].get_rect(topleft=(10, 10)) for i in range(pages_num)]  # прямоугольник картинки
    screen.blit(screen_img, (0, 0))
    screen.blit(latex[curr_img], lr[curr_img])  # вывод картинки

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

            if abs(scroll_counter) >= scrolls_to_change:
                curr_img += sign(scroll_counter)
                scroll_counter = 0
                page_upd()

            manager.process_events(event)
        if not is_running:
            break

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


if __name__ == '__main__':
    ls = ['$y=1$']  # , '$y=x$', '$y=x^2$', '$y=x^3$', '$y=x^4$'
    export(ls)
