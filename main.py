import sys

from load_graph import *
from find_edges import *
from gui import *
from get_chrome_history import *


DEBUG = True

if __name__ == "__main__":
    try:
        get_history()
        FILE_NAME = 'out.csv'
    except:# OperationalError:
        print("Chrome database could not be accessed.. Using demo history file")
        FILE_NAME = 'history.csv'

    g, md = load_graph(FILE_NAME)
    g = find_edges(g, md)

    gui = Gui(g, md)

    gui.draw()  # draw once only since the graph does not change
    # The event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and
                    (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
            # Respond to clicks
                gui.on_click(event)
            elif event.type == pygame.MOUSEMOTION:
            # Respond to moves
                gui.on_move(event)