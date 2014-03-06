__author__ = 'jankiel'

import matplotlib.pyplot as plt
import pygame
import pygame.gfxdraw
from pygame.locals import *

def plotData(data):
    plt.plot(range(data), data)

def show():
    plt.show()


class Button:
    hovered = False

    def __init__(self, text, pos, event=None):
        self.text = text
        self.pos = pos
        self.menu_font = pygame.font.Font(None, 40)
        self.set_rect()
        self.event = event if event else lambda: None

    def draw(self, surface):
        self.set_rend()
        surface.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (180, 180, 180)
        else:
            return (100, 100, 100)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


class MapCreator2000():
    def __init__(self, w=None, h=None):
        self.points = []
        self.w = w if w else 800
        self.h = h if h else 600
        pygame.init()       # inicjalizuj biblioteke pygame
        pygame.display.set_mode((self.w, self.h))#stwórz okno
        self.surface = pygame.display.get_surface()
        compute = Button('Oblicz trasę', (20, self.h - 40), self.solve)
        clear = Button('Wyczyść', (compute.rect.right+20, self.h - 40), self.clear)
        exit = Button('Wyjdź', (clear.rect.right+20, self.h - 40), self.exit)
        self.buttons = [compute, clear, exit]
        self.bounding_box = pygame.Rect(0, self.h-50, self.buttons[-1].rect.right+20, 50)
        self.gamestate = True
        self.loop()         # glowna petla gry

    def check_clicked(self):
        for b in self.buttons:
            if b.hovered:
                b.event()

    def set_circle(self, pos):
        self.points.append((pos[0] + 5, pos[1] + 5))

    def solve(self):
        print('tu idzie solver')

    def clear(self):
        self.points = []

    def exit(self):
        self.gamestate = False

    def draw(self):
        self.surface.fill((255, 255, 255))
        for p in self.points:
            pygame.gfxdraw.aacircle(self.surface, p[0] - 5, p[1] - 5, 5, (0, 0, 0))
            pygame.gfxdraw.filled_circle(self.surface, p[0] - 5, p[1] - 5, 5, (0, 0, 0))
        for b in self.buttons:
            b.draw(self.surface)
        pygame.draw.rect(self.surface, (0,0,0), self.bounding_box, 2)
        pygame.display.flip()

    def checkMenu(self):
        for b in self.buttons:
            if b.rect.collidepoint(pygame.mouse.get_pos()):
                b.hovered = True
            else:
                b.hovered = False

    def loop(self):
        clock = pygame.time.Clock()

        while self.gamestate:
            clock.tick(60)
            self.checkMenu()
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.gamestate = False
                elif event.type == MOUSEBUTTONUP:
                    if not self.bounding_box.collidepoint(event.pos):
                        self.set_circle(event.pos)
                    else:
                        self.check_clicked()#tu jeszcze sprawdzenie nacisniecia przycisku

                self.draw()


if __name__ == "__main__":
    m = MapCreator2000()
    print('ale nadal mam ', m.points)

