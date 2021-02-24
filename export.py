import win32api  # pywin32
import pygame_gui  # pygame-gui
import pygame  # pygame
import matplotlib.pyplot as plt  # matplotlib
from PIL import Image  # pillow
import os  # os
from fpdf import FPDF  # PyFPDF
import fitz  # PyMuPDF

# consts
save_name = 'задания'  # имя сохранения, по умолчанию - 'задания'


#  TODO: динамический интерфейс 1
#  TODO: несколько страниц проверить 7
#  TODO: латех хотя бы чек 7
#  TODO: чек pyqt 7
# картинка на кнопку 7

#  fixme: большие тексты с формулами 3
def export(latex_string):
    """функция принимает текст LaTex'а, заключенный в доллары, и занимается выводом
        баги: слетает кодировка, не работает с большими текстами"""
    fig = plt.figure()  # используем matplotlib для перобразования
    ax = fig.add_axes([0, 0, 1, 1])  # LaTeX в картинку
    ax.set_axis_off()
    ax.text(0.5, 0.5, latex_string,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color='black')

    plt.savefig('latex.png')  # временная картинка

    image = Image.open('latex.png')  # обрезаем картинку с помощью PIL
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
    image.save("latex.png")

    pdf = FPDF()  # создаем временный pdf с помощью PyFPDF
    pdf.add_page()  # добавляем страницу
    pdf.image('latex.png', x=10, y=8)  # вставляем картинку
    pdf.output("latex.pdf")  # сохраняем

    pdffile = 'latex.pdf'  # чтобы сделать png размера A4
    doc = fitz.open(pdffile)
    page = doc.loadPage(0)
    pix = page.getPixmap()
    pix.writePNG('latex_A4.png')
    doc.close()

    pygame.init()  # запускаем pygame
    pygame.font.init()
    manager = pygame_gui.UIManager((580, 540), 'theme.json')
    infoObject = pygame.display.Info()  # информация о экране
    screen = pygame.display.set_mode((580, 540))  # окно
    screen_img = pygame.image.load("files/ground.jpg")
    screen.blit(screen_img, (0, 0))

    # TODO: норм качество 3
    latex = pygame.image.load('latex_A4.png')  # загружаем картинку
    latex = pygame.transform.scale(latex, (370, int(370 * 2 ** 0.5)))  # меняем размер
    lr = latex.get_rect(topleft=(10, 10))  # прямоугольник картинки
    screen.blit(latex, lr)  # вывод картинки

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

    def save_png(name):  # сохранение в png
        """Функция принимает имя для сохранения
            Функция копирует временный .png файл и переименовывает.
            Также меняет цвет кнопки сохранения в png на более светлый """
        os.popen(f'copy latex.png {name}.png')
        save_png_button.disable()

    def open_png(name):
        os.popen(f'copy latex.png {name}.png')
        save_png_button.disable()
        open_png_button.disable()
        os.system(os.getcwd() + f'\\{name}.png')

    def save_pdf(name):  # сохранение в pdf
        """Функция принимает имя для сохранения
            Функция копирует временный .pdf файл и переименовывает.
            Также меняет цвет кнопки сохранения в pdf на более светлый"""
        os.popen(f'copy latex.pdf {name}.pdf')
        save_pdf_button.disable()

    def open_pdf(name):
        os.popen(f'copy latex.pdf {name}.pdf')
        save_png_button.disable()
        open_png_button.disable()
        os.system(os.getcwd() + f'\\{name}.pdf')

    def printer():
        win32api.ShellExecute(0, 'print', os.getcwd() + '\\latex.pdf', '.', '/manualstoprint', 0)  # по идее так

    save_png_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((395, 10), (170, 30)),
                                                   text='сохранить в png', manager=manager)

    open_png_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((395, 50), (170, 30)),
                                                   text='в png и открыть', manager=manager)

    save_pdf_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((395, 90), (170, 30)),
                                                   text='сохранить в pdf', manager=manager)

    open_pdf_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((395, 130), (170, 30)),
                                                   text='в pdf и открыть', manager=manager)

    print_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((395, 170), (170, 30)),
                                                text='печать', manager=manager)

    name_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((395, 230), (170, 20)),
                                                       manager=manager)
    name_textbox.set_text(save_name)

    name_label = pygame.font.SysFont('Calibri', 14)
    name_label = name_label.render('Имя сохранения:', True, (0, 0, 0))
    screen.blit(name_label, (400, 213))
    clock = pygame.time.Clock()

    is_running = True
    while is_running:  # обработка выхода из окна
        time_delta = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                os.remove('latex.png')
                os.remove('latex.pdf')
                os.remove('latex_A4.png')
                break

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == save_png_button:
                        save_png(save_name)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == open_png_button:
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

            manager.process_events(event)
        if not is_running:
            break

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


if __name__ == '__main__':
    export('$y=x^2$')
