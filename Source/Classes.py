import pygame, math

class figure(pygame.sprite.Sprite):
    def __init__(self, img, posX, posY):
        super().__init__()
        self.img = img
        self.rect = pygame.Rect(posX, posY, self.img.get_width(), self.img.get_height())

class board(pygame.sprite.Sprite):
    def __init__(self, scale, posX, posY, makeTransparentAfterWinning):
        super().__init__()
        self.makeTransparentAfterWinning = makeTransparentAfterWinning
        self.VictoryCoordinates1 = [0, 2, 0, 1, 2, 0, 3, 6]
        self.VictoryCoordinates2 = [4, 4, 3, 4, 5, 1, 4, 7]
        self.VictoryCoordinates3 = [8, 6, 6, 7, 8, 2, 5, 8]
        self.rect = pygame.Rect(posX, posY, 102 * scale, 102 * scale)
        self.status = [""] * 9
        self.figures = pygame.sprite.Group()
        self.scale = scale
        self.avalible =  True
        self.placing =  True
        self.crossORG = pygame.image.load('Textures/Cross.png')
        self.circleORG = pygame.image.load('Textures/Circle.png')
        self.frameORG = pygame.image.load('Textures/Frame.png')
        self.cross = pygame.transform.scale(self.crossORG, ((self.crossORG.get_width() / 8) * self.scale, (self.crossORG.get_height() / 8) * self.scale))
        self.circle = pygame.transform.scale(self.circleORG, ((self.circleORG.get_width() / 8) * self.scale, (self.circleORG.get_height() / 8) * self.scale))
        self.frame = pygame.transform.scale(self.frameORG, (106 * scale, 106 * scale))
        self.slots = [
            (self.rect.x, self.rect.y),
            (self.rect.x + self.rect.w / 2.914, self.rect.y),
            (self.rect.x + (self.rect.w / 2.914) * 2, self.rect.y),
            (self.rect.x, self.rect.y + self.rect.h / 2.914),
            (self.rect.x + self.rect.w / 2.914, self.rect.y + self.rect.h / 2.914),
            (self.rect.x + (self.rect.w / 2.914) * 2, self.rect.y + self.rect.h / 2.914),
            (self.rect.x, self.rect.y + (self.rect.h / 2.914) * 2),
            (self.rect.x + self.rect.w / 2.914, self.rect.y + (self.rect.h / 2.914) * 2),
            (self.rect.x + (self.rect.w / 2.914) * 2, self.rect.y + (self.rect.h / 2.914) * 2)
        ]

    def place(self, position, player):
        self.status[position] = player
    def updateVisuals(self):
        try:
            self.figures.empty()
        except:
            pass
        for item, id in zip(self.status, range(9)):
            if item == "":
                continue
            elif item == "X":
                self.newFigure = figure(self.cross, self.slots[id][0], self.slots[id][1])
                self.figures.add(self.newFigure)
            elif item == "O":
                self.newFigure = figure(self.circle, self.slots[id][0], self.slots[id][1])
                self.figures.add(self.newFigure)

    def checkDraw(self):
        if self.status[0] != "" and self.status[1] != "" and self.status[2] != "" and self.status[3] != "" and self.status[4] != "" and self.status[
            5] != "" and self.status[6] != "" and self.status[7] != "" and self.status[8] != "":
            self.avalible = False

    def checkVictory(self):
        for i in range(8):
            if self.status[self.VictoryCoordinates1[i]] == "X" and self.status[self.VictoryCoordinates2[i]] == "X" and self.status[self.VictoryCoordinates3[i]] == "X":
                self.avalible = False
                if self.makeTransparentAfterWinning == True:
                    for figure in self.figures:
                        self.cross.set_alpha(85)
                        self.circle.set_alpha(85)
                return "X"
            else:
                if self.status[self.VictoryCoordinates1[i]] == "O" and self.status[self.VictoryCoordinates2[i]] == "O" and self.status[self.VictoryCoordinates3[i]] == "O":
                    self.avalible = False
                    if self.makeTransparentAfterWinning == True:
                        for figure in self.figures:
                            self.cross.set_alpha(85)
                            self.circle.set_alpha(85)
                    return "O"
                else:
                    self.checkDraw()