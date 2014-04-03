from load_graph import *
from find_edges import *
from gui import *
import sys

DEBUG = True
FILE_NAME = 'history.csv'

if __name__ == "__main__":
    g, md = load_graph(FILE_NAME)
    g = find_edges(g, md)

    BG_COLOR = (50, 50, 50)
    LINE_COLOR = (255, 0, 0)
    TEXT_COLOR = (0, 0, 255)
    TEXT_BG_COLOR = (25, 25, 25)
    gui = Gui(g, md, BG_COLOR, LINE_COLOR, TEXT_COLOR, TEXT_BG_COLOR)

    gui.draw()
    # The main loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and
                         (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                pygame.display.quit()
                sys.exit()
            # Respond to clicks
            elif event.type == pygame.MOUSEBUTTONUP:
                gui.on_click(event)
            # Respond to moves
            elif event.type == pygame.MOUSEMOTION:
                gui.on_move(event)