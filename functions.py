from PIL import Image
from tkinter import Tk, filedialog
import os
import pygame

Tk().withdraw()

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                            title = "Select a file",
                                            filetypes = (('Png files', '*.png'),
                                                            ('JPEG files', '*.jpeg'))
                                                            )

    return filename


def getTiles(tileImage, pixels = (32, 32)):
    width, height = tileImage.size
    images = []
    for w in range(width//pixels[0]):
        for h in range(height//pixels[1]):
            cropped_img = tileImage.crop((w*pixels[0], h*pixels[1], w*pixels[0]+pixels[0], h*pixels[1]+pixels[1]))
            pix, col, *rem = cropped_img.getcolors()[0]
            if not (pix == pixels[0]*pixels[1] and col == (0, 0, 0, 0)):
                images.append(cropped_img)

    return images

def makeTileSurface(tiles, size = (200, 100)):
    surface = pygame.Surface(size)

    col = 0
    row = 0
    for tile in tiles:
        if row == 3:
            row = 0
        mode = tile.mode
        size = tile.size
        data = tile.tobytes()
        py_image = pygame.image.fromstring(data, size, mode)
        surface.blit(py_image, (col*size[0]+1, size[1]*row+1))
        row += 1
        if row%3 == 0:
            col += 1

    pygame.draw.rect(surface, (255, 0, 0), (2, 2, 194, 96), 2)

    return surface

def makeMapSurface(mapSize, gridSize):
    pass

tileFile = None

screen = pygame.display.set_mode((1024, 512))
clock = pygame.time.Clock()

run = True
while run:

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (220, 20, 100, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            xPos = mousePos[0] > 220 and mousePos[0] < 320
            yPos = mousePos[1] > 20 and mousePos[1] < 70

            if all([xPos, yPos]):
                tileFile = browseFiles()
                if tileFile == '':
                    tileFile = None
                    break
                tileImg = Image.open(tileFile)
                tiles = getTiles(tileImg)
                tileMenu = makeTileSurface(tiles)

    if tileFile is not None:
        screen.blit(tileMenu, (0, 0))

    pygame.display.update()
