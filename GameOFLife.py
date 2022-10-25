import time
from turtle import position
import pygame
import numpy as np
import button

pygame.init()

BackGRD_Blk = (10, 10, 10) #Black
GRID_BlkGry = (40,40,40) #BlackGray
Die_Next_LghtGry = (170,170,170) #lightGray
ALIVE_Next_Wht = (255,255,255) #white
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

screen = pygame.display.set_mode((800, 755))

pygame.display.set_caption('GAME OF LIFE                                  [SPACEBAR] for PAUSE/PLAY')

start_img = pygame.image.load("start_button.png").convert_alpha()
exit_img = pygame.image.load("exit_button.png").convert_alpha()

#button class
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and click conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#creat button instances
start_button = Button(300, 355, start_img, 0.5)
exit_button = Button(310, 700, exit_img, 0.5)

def update(screen, cells, size, with_progress=False):
    update_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = BackGRD_Blk if cells[row, col] == 0 else ALIVE_Next_Wht

        #Game rules
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = Die_Next_LghtGry

            elif 2 <= alive <= 3:
                update_cells[row, col] =  1
                if with_progress:
                    color = ALIVE_Next_Wht
        else:
            if alive == 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = ALIVE_Next_Wht

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size -1))

    return update_cells


def main():
    pygame.init()

    cells = np.zeros((70, 80)) # grids 70x80
    screen.fill(GRID_BlkGry) #Grid color as background
    
    update(screen, cells, 10)
    start_button.draw()
    pygame.display.flip()
    pygame.display.update()
    
    running = False
    #set the quit and pause command
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            # Uses Spacebare for Action
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            # Look for square to turn    
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1]//10, pos[0]//10] = 1
                update(screen, cells, 10)
                pygame.display.update()  

        screen.fill(GRID_BlkGry)

        #cells updated with the return value
        if running:
            cells = update(screen, cells, 10, with_progress=True)
            exit_button.draw()
            if exit_button.draw():
                run = False
            pygame.display.update()
        time.sleep(0.001)    

if __name__ == '__main__':
    main()
