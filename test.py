import pygame
import matplotlib.pyplot as plt
from PIL import Image
import os

s = r''
f = open('latex.txt')
for i in f:
    s += i
f.close()

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()
t = ax.text(0.5, 0.5, s,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color='black')

plt.savefig('latex.png')

image = Image.open('latex.png')
pix = image.load()
x1, y1, x2, y2 = image.size[0], image.size[1], 0, 0,
for x in range(image.size[0]):
    for y in range(image.size[1]):
        if pix[x, y][0] < 255 or pix[x, y][1] < 255 or pix[x, y][2] < 255:
            x1 = min(x, x1)
            y1 = min(y, y1)
            x2 = max(x, x2)
            y2 = max(y, y2)
image = image.crop((x1 - 3, y1 - 3, x2 + 3, y2 + 3))
image.save("latex.png")

pygame.init()
screen = pygame.display.set_mode((600, 500))
screen.fill((200, 200, 200))

latex = pygame.image.load('latex.png')
latex.set_colorkey((255, 255, 255))
lr = latex.get_rect(
    center=(300, 250))
screen.blit(latex, lr)

pygame.display.update()

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            os.remove('latex.png')



