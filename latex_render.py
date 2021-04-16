import argparse
from matplotlib import pyplot as plt
import matplotlib
from PIL import Image
import subprocess

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = r'''\usepackage{amsmath}
\usepackage[russian]{babel}'''
parser = argparse.ArgumentParser()
parser.add_argument('--dpi', default='300')  # аргумент командной строки - качество
parser.add_argument('--fs', default='15')  # аргумент командной строки - размер шрифта
parser.add_argument('--name', default='')  # аргумент командной строки - название картинки - latex+name
parser.add_argument('--ls')  # аргумент командной строки - строка для рендера
args = parser.parse_args()


def create_latex(latex_string=args.ls, name=args.name, font_size=int(args.fs), dpi=int(args.dpi)):
    plt.figure(1)
    ax = plt.axes()
    ax.set_axis_off()
    ax.text(0.5, 0.5, latex_string,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=font_size, color='black')
    plt.savefig(f'temp_files/latex{name}.png', bbox_inches='tight', dpi=dpi)
    plt.close()


# TODO: ускорить обрезку
def crop_latex(name=args.name):
    image = Image.open(f'temp_files/latex{name}.png')  # обрезаем картинку с помощью PIL
    pix = image.load()  # массив пикселей
    x1, y1, x2, y2 = 0, 0, image.size[0] - 1, image.size[1] - 1
    flag = False
    while x1 < image.size[0] - 1:
        for y in range(image.size[1]):
            if pix[x1, y][0] < 255 or pix[x1, y][1] < 255 or pix[x1, y][2] < 255:
                flag = True
                break
        if flag:
            break
        x1 += 1
    flag = False
    while x2 > x1:
        for y in range(image.size[1]):
            if pix[x2, y][0] < 255 or pix[x2, y][1] < 255 or pix[x2, y][2] < 255:
                flag = True
                break
        if flag:
            break
        x2 -= 1
    flag = False
    while y1 < image.size[0] - 1:
        for x in range(x1, x2 + 1):
            if pix[x, y1][0] < 255 or pix[x, y1][1] < 255 or pix[x, y1][2] < 255:
                flag = True
                break
        if flag:
            break
        y1 += 1
    flag = False
    while y2 > y1:
        for x in range(x1, x2 + 1):
            if pix[x, y2][0] < 255 or pix[x, y2][1] < 255 or pix[x, y2][2] < 255:
                flag = True
                break
        if flag:
            break
        y2 -= 1
    image = image.crop((max(x1 - 3, 0), max(y1 - 3, 0), min(x2 + 3, image.size[0] - 1),
                        min(y2 + 3, image.size[1] - 1)))  # немного оставил запас
    image.save(f"temp_files/latex{name}.png")
    f = open(f'temp_files/dim{name}.txt', 'w')
    print(str(x2 - x1 + 6), file=f)
    print(str(y2 - y1 + 6), file=f)
    f.close()


create_latex()
crop_latex()
