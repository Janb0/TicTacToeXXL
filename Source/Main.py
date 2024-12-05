import time

import pygame, math
from Classes import board

pygame.display.init()
pygame.font.init()


ScreenSize = pygame.display.get_desktop_sizes()
print(ScreenSize)
FPS = 30
gameOn = True
currentTurn = 0
displayTurn = 0
currentFigure = {
    0 : "O",
    1 : "X"
}


canvas = pygame.display.set_mode(ScreenSize[0])
pygame.display.toggle_fullscreen()
clock = pygame.time.Clock()
scale = ScreenSize[0][0] / 192
print(scale)
font = pygame.font.SysFont('Bahnschrift', round(5 * scale))
fontBig = pygame.font.SysFont('Bahnschrift', round(10 * scale))
fontColor = (0,0,0)

backgroundORG = pygame.image.load('textures/bg.png')
background = pygame.transform.scale(backgroundORG, (backgroundORG.get_width() * scale, backgroundORG.get_height() * scale))

mainBoard = board(scale, 45 * scale, 3 * scale, False)
boards = pygame.sprite.Group()
for i in range(9):
    newBoard = board(scale / 3.185, mainBoard.slots[i][0], mainBoard.slots[i][1], True)
    boards.add(newBoard)

def detectWhichBoardDoesMouseTouch():
    for i in boards:
        if i.rect.collidepoint(pygame.mouse.get_pos()):
            return i.rect

def placeOnEveryBoard():
    for board in boards:
        if board.avalible:
            board.placing = True
        else:
            board.placing = False

def movePlacement(dest):
    for board in boards:
        if math.floor(mainBoard.slots[dest][0]) == board.rect.x and math.floor(mainBoard.slots[dest][1]) == board.rect.y:
            if not board.avalible:
                placeOnEveryBoard()
                break
            else:
                board.placing = True
        else:
            board.placing = False
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameOn = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == True:
                for board in boards:
                    if board.rect == detectWhichBoardDoesMouseTouch() and board.placing:
                        slotCenterDist = []
                        for i in board.slots:
                            slotCenterDist.append(math.dist((i[0] + board.rect.w * (4.5 / 32), i[1] + board.rect.h * (4.5 / 32)), pygame.mouse.get_pos()))
                        newFigurePlacePos = slotCenterDist.index(min(slotCenterDist))
                        if board.status[newFigurePlacePos] == "":
                            currentTurn += 1
                            board.place(newFigurePlacePos, currentFigure[currentTurn % 2])
                            board.checkVictory()
                            movePlacement(newFigurePlacePos)
                            board.updateVisuals()

    mainBoard.updateVisuals()
    canvas.blit(background, (0, 0))
    displayTurn = math.floor((currentTurn) / 2) + 1

    for board, i in zip(boards, range(9)):
        if not board.avalible:
            mainBoard.place(i, board.checkVictory())
            mainBoard.updateVisuals()
        for figure in board.figures:
            canvas.blit(figure.img, figure.rect)
        if board.placing:
            canvas.blit(board.frame, (board.rect.x - 2 * board.scale, board.rect.y - 2 * board.scale))

    for figure in mainBoard.figures:
        canvas.blit(figure.img, figure.rect)

    canvas.blit(font.render(f'Tura: {displayTurn}', True, fontColor), (5 * scale, 90 * scale))
    canvas.blit(font.render(f'Nastepny:', True, fontColor), (5 * scale, 100 * scale))
    if currentFigure[currentTurn % 2] == "O":
        canvas.blit(pygame.transform.scale(pygame.image.load('Textures/Cross.png'), (5 * scale, 5 * scale)), (30 * scale, 100 * scale))
    else:
        canvas.blit(pygame.transform.scale(pygame.image.load('Textures/Circle.png'), (5 * scale, 5 * scale)), (30 * scale, 100 * scale))
    if mainBoard.checkVictory() != None:
        canvas.blit(fontBig.render(f'Wygral {mainBoard.checkVictory()}!', True, fontColor), (149 * scale, 50 * scale))
        for board in boards:
            board.placing = False

    pygame.display.flip()
    clock.tick(FPS)