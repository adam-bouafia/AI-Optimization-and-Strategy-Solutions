import pygame.font


class Button:

    def __init__(self, display=None, top=0, left=0, w=0, h=0,
                 borderColor=(64,201,209), selectedBorderColor=(178,3,60),
                 text='', font='comicsansms', fontDimension=24,
                 textColor=(255,228,196), value=''):
        self.display = display
        self.borderColor = borderColor
        self.selectedBorderColor = selectedBorderColor
        self.text = text
        self.font = font
        self.width = w
        self.height = h
        self.selected = False
        self.fontDimension = fontDimension
        self.textColor = textColor
        self.top = top
        self.left = left

        fontObj = pygame.font.SysFont(self.font, self.fontDimension)
        self.renderedText = fontObj.render(self.text, True, self.textColor)
        self.rectangle = pygame.Rect(left, top, w, h)
        self.rectangleText = self.renderedText.get_rect(center=self.rectangle.center)
        self.value = value

    def select(self, selected):
        self.selected = selected
        self.draw()

    def selectByCoord(self, coord):
        if self.rectangle.collidepoint(coord):
            self.select(True)
            return True
        return False

    def updateRectangle(self):
        self.rectangle.left = self.left
        self.rectangle.top = self.top
        self.rectangleText = self.renderedText.get_rect(center=self.rectangle.center)

    def draw(self):
        if self.selected:
            borderColor = self.selectedBorderColor
        else:
            borderColor = self.borderColor

        border_radius = int(min(self.width, self.height) / 2)
        pygame.draw.rect(self.display, borderColor, self.rectangle, 1, border_radius=border_radius)
        self.display.blit(self.renderedText, self.rectangleText)

