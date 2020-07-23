from pygame import image, display, surface
from math import sqrt
from time import sleep


class button:
    def __init__(self, name):
        self.name = name
        x = name.split(".")
        self.namep = x[0] + "p." + x[1]

        try:
            self.img = image.load(self.name)
            self.img2 = image.load(self.namep)
        except:
            raise FileNotFoundError(
                f"The file named {self.name} or {self.namep} was not found.")

        self.rect = self.img.get_rect()
        self.x = 0
        self.y = 0

    def bindFun(self, fun):
        self.fun = fun

    def __imgUpdate(self, win):
        win.blit(self.img2, (self.x, self.y))
        display.update()
        sleep(0.5)
        win.blit(self.img, (self.x, self.y))
        self.fun()

    def fun_if_pressed(self, mcoords, win):
        mx, my = mcoords
        x, y = self.x, self.y
        b = 40
        l = 120
        if ((mx >= x) and (mx <= (x+l))):
            if ((my >= y) and (my <= (y+b))):
                self.__imgUpdate(win)


class Block:
    def __init__(self, block_num):
        if ((block_num >= 0) and (block_num < 16)):

            self.name = f"images/img{block_num}.png"

            try:
                self.img = image.load(self.name)
            except:
                raise FileNotFoundError(
                    f" a file named {self.name} was not found.")

            self.block_num = block_num
            self.rect = self.img.get_rect()

        else:
            raise FileExistsError(
                f"The image associated to {block_num} could not be found.")

    def get_distance(self, BlockObj):
        a = self.rect.center
        b = BlockObj.rect.center
        dist = sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
        return dist
