import pygame
import matplotlib.pyplot as plt
from PIL import Image
import os
import pygame_widgets as pw

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
image = image.crop((x1 - 3, y1 - 3, x2 + 3, y2 + 3))  # немного оставил с запасом
image.save("latex.png")

pygame.init()  # запускаем pygame
infoObject = pygame.display.Info()  # информация о экране
screen = pygame.display.set_mode((500, 474))  # окно
screen.fill((200, 200, 200))  # я сделал серый, т. к. белый яркий
pygame.draw.rect(screen, (255, 255, 255), (10, 10, 300, 424))

latex = pygame.image.load('latex.png')  # загружаем картинку
os.remove('latex.png')  # удаляем временный файл
latex.set_colorkey((255, 255, 255))
lr = latex.get_rect(topleft=(20, 20))  # прямоугольник картинки
screen.blit(latex, lr)  # вывод картинки

save_png_button = pw.Button(  # кнопка сохранения в png
    screen, 320, 10, 170, 30, text='Сохранить в png',
    fontSize=20, margin=20,
    inactiveColour=(180, 180, 180),
    hoverColour=(160, 160, 160),
    pressedColour=(0, 255, 0),
    onClick=lambda: print('Сохранить в png'))

save_pdf_button = pw.Button(  # кнопка сохранения в pdf
    screen, 320, 50, 170, 30, text='Сохранить в pdf',
    fontSize=20, margin=20,
    inactiveColour=(180, 180, 180),
    hoverColour=(160, 160, 160),
    pressedColour=(0, 255, 0),
    onClick=lambda: print('Сохранить в pdf'))

print_button = pw.Button(  # кнопка печати
    screen, 320, 90, 170, 30, text='Печать',
    fontSize=20, margin=20,
    inactiveColour=(180, 180, 180),
    hoverColour=(160, 160, 160),
    pressedColour=(0, 255, 0),
    onClick=lambda: print('Печать'))

while 1:  # обработка выхода из окна
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
    save_png_button.listen(pygame.event.get())  # обработка кнопок
    save_png_button.draw()
    save_pdf_button.listen(pygame.event.get())
    save_pdf_button.draw()
    print_button.listen(pygame.event.get())
    print_button.draw()
    pygame.display.update()
