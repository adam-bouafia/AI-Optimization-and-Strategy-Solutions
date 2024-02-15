import math
import sys

from Button import *
from ButtonGroup import *

buttonHeight = 50
algButtonWidth = 170
playerButtonWidth = 100
startButtonWidth = 110
difficultyButtonWidth = 200
gametypeButtonWidth = 300
topMargin = 30

pygame.mixer.init()
pygame.mixer.music.load('assets/audio/hexaudio.mp3')
pygame.mixer.music.play(-1)
def homePage(game, display):
    algorithm = ButtonGroup(
        top=topMargin,
        left=game.screenSize[0] / 2 - algButtonWidth,
        buttonList=[
            Button(display=display, w=algButtonWidth, h=buttonHeight, text="Minimax", value="minimax"),
            Button(display=display, w=algButtonWidth, h=buttonHeight, text="Alpha-Beta", value="alphabeta")
        ],
        selected=1
    )
    player = ButtonGroup(
        top=2*topMargin + buttonHeight,
        left=game.screenSize[0] / 2 - playerButtonWidth,
        buttonList=[
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Red", value="red"),
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Blue", value="blue")
        ],
        selected=0
    )
    difficulty = ButtonGroup(
        top=3*topMargin + 2*buttonHeight,
        left=game.screenSize[0] / 2.55 - difficultyButtonWidth,
        buttonList=[
            Button(display=display, w=difficultyButtonWidth, h=buttonHeight,
                   text="Beginner", value="beginner"),
            Button(display=display, w=difficultyButtonWidth, h=buttonHeight,
                   text="Medium", value="medium"),
            Button(display=display, w=difficultyButtonWidth, h=buttonHeight,
                   text="Advanced", value="advanced")
        ],
        selected=0
    )
    gameType = ButtonGroup(
        top=4*topMargin + 3*buttonHeight,
        left=game.screenSize[0] / 2 - gametypeButtonWidth,
        buttonList=[
            Button(display=display, w=gametypeButtonWidth, h=buttonHeight,
                   text="Player vs Player", value="pvp"),
            Button(display=display, w=gametypeButtonWidth, h=buttonHeight,
                   text="Player vs Computer", value="pve")
        ],
        selected=1
    )
    start = Button(display=display,
                   top=5*topMargin + 4*buttonHeight,
                   left=game.screenSize[0] / 2 - startButtonWidth / 2 + 35,
                   w=startButtonWidth,
                   h=buttonHeight,
                   text="START")
    quitbtn = Button(display=display,
                     top=6*topMargin + 5*buttonHeight,
                     left=game.screenSize[0] / 2 - startButtonWidth / 2 + 35,
                     w=startButtonWidth,
                     h=buttonHeight,
                     text="QUIT")
    background = pygame.image.load('assets/image/bg.png')
    screen_size = pygame.display.get_surface().get_size()
    scaled_background = pygame.transform.scale(background, screen_size)
    display.blit(scaled_background, (0, 0))
    algorithm.draw()
    player.draw()
    difficulty.draw()
    gameType.draw()
    start.draw()
    quitbtn.draw()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if quitbtn.selectByCoord(pos):
                    pygame.quit()
                    sys.exit(0)
                if not algorithm.selectByCoord(pos):
                    if not player.selectByCoord(pos):
                        if not difficulty.selectByCoord(pos):
                            if not gameType.selectByCoord(pos):
                                if start.selectByCoord(pos):
                                    return player.getValue(), algorithm.getValue(), \
                                           difficulty.getValue(), gameType.getValue()
        pygame.display.update()


def computeTileDimensions(size):
    return size * math.sqrt(3), size * 2


def cornerPoint(radius, index, pos):
    deg = 60 * index + 30
    theta = math.pi / 180 * deg
    x, y = pos
    return radius * math.cos(theta) + x, radius * math.sin(theta) + y


def integer(number):
    try:
        int(number)
        return True
    except ValueError:
        return False
