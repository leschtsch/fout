import pygame
import matplotlib.pyplot as plt
from PIL import Image
import os
import pygame_widgets as pw
from fpdf import FPDF
import fitz

#  TODO: большие тексты с формулами
latex_string = r''  # строка LaTeX для вывода
latex_file = open('latex.txt')  # файл с LaTeX формулой
for i in latex_file:
    latex_string += i
latex_file.close()

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
pdf.image('latex.png', x=10, y=8, w=100)  # вставляем картинку
pdf.output("latex.pdf")  # сохраняем

pdffile = 'latex.pdf'  # чтобы сделать png размера A4
doc = fitz.open(pdffile)
page = doc.loadPage(0)
pix = page.getPixmap()
pix.writePNG('latex_A4.png')
doc.close()

pygame.init()  # запускаем pygame
infoObject = pygame.display.Info()  # информация о экране
screen = pygame.display.set_mode((580, 540))  # окно
screen.fill((200, 200, 200))  # я сделал серый, т. к. белый яркий

latex = pygame.image.load('latex_A4.png')  # загружаем картинку
latex = pygame.transform.scale(latex, (370, int(370 * 2 ** 0.5)))  # меняем размер
lr = latex.get_rect(topleft=(10, 10))  # прямоугольник картинки
screen.blit(latex, lr)  # вывод картинки


def p():  # latex:pass не работает
    """функция не делает ничего"""
    pass


def save_png(name):  # сохранение в png
    """Функция копирует временный .png файл  переименовывает.
        Также меняет цвет кнопки сохранения в png на более светлый """
    os.popen(f'copy latex.png {name}.png')
    save_png_button.inactiveColour = (190, 190, 190)  # делаем кнопку неактивной
    save_png_button.hoverColour = (190, 190, 190)
    save_png_button.pressedColour = (190, 190, 190)
    save_png_button.onClick = lambda: p()


def save_pdf(name):  # сохранение в pdf
    """Функция копирует временный .pdf файл  переименовывает.
        Также меняет цвет кнопки сохранения в pdf на более светлый"""
    os.popen(f'copy latex.pdf {name}.pdf')
    save_pdf_button.inactiveColour = (190, 190, 190)  # делаем кнопку неактивной
    save_pdf_button.hoverColour = (190, 190, 190)
    save_pdf_button.pressedColour = (190, 190, 190)
    save_pdf_button.onClick = lambda: p()


save_png_button = pw.Button(  # кнопка сохранения в png
    screen, 395, 10, 170, 30, text='Сохранить в png',
    fontSize=20, margin=20,
    inactiveColour=(180, 180, 180),
    hoverColour=(160, 160, 160),
    pressedColour=(140, 140, 140),
    onClick=lambda: save_png('формула'))

save_pdf_button = pw.Button(  # кнопка сохранения в pdf
    screen, 395, 50, 170, 30, text='Сохранить в pdf',
    fontSize=20, margin=20,
    inactiveColour=(180, 180, 180),
    hoverColour=(160, 160, 160),
    pressedColour=(140, 140, 140),
    onClick=lambda: save_pdf('формула'))

#  TODO: печать
print_button = pw.Button(  # кнопка печати
    screen, 395, 90, 170, 30, text='Печать',
    fontSize=20, margin=20,
    inactiveColour=(180, 180, 180),
    hoverColour=(160, 160, 160),
    pressedColour=(140, 140, 140),
    onClick=lambda: print('Печать'))

while 1:  # обработка выхода из окна
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            os.remove('latex.png')
            os.remove('latex.pdf')
            os.remove('latex_A4.png')
    save_png_button.listen(pygame.event.get())  # обработка кнопок
    save_png_button.draw()
    save_pdf_button.listen(pygame.event.get())
    save_pdf_button.draw()
    print_button.listen(pygame.event.get())
    print_button.draw()
    pygame.display.update()
