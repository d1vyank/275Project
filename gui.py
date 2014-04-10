import random
import math
import webbrowser

import pygame

from graph import least_cost_path



# the dimension for each icon on screen
IMG_WIDTH = 32
IMG_HEIGHT = IMG_WIDTH

# the dimension for the graph area on screen (canvas size for the icons and edges)
GRAPH_WIDTH = 800
GRAPH_HEIGHT = GRAPH_WIDTH

# the dimension for the infobox area on screen (text info at the bottom)
INFO_WIDTH = GRAPH_WIDTH
INFO_HEIGHT = 30

# these values will be used to determine the total size of the screen
TOTAL_WIDTH = GRAPH_WIDTH
TOTAL_HEIGHT = GRAPH_HEIGHT + INFO_HEIGHT

# the thickness of an edge on screen
LINE_THICKNESS = 1

# the default message in the infobox
INFO_PROMPT = "Hover: view title; left click: least cost path; right click: launch link in browser."

BG_COLOR = (50, 50, 50)  # darkish (background for the graph canvas)
LINE_COLOR = (255, 0, 0)  # red (edge)
TEXT_COLOR = (0, 0, 255)  # blue (text on the infobox canvas)
TEXT_BG_COLOR = (25, 25, 25)  # blackish (background for the infobox canvas)
ACCENT_COLOR = (0, 255, 0)  # green (for outline-ing selected icons and edges)


class Gui:
    def __init__(self, graph, md, bg_color=BG_COLOR, line_color=LINE_COLOR,
                 text_color=TEXT_COLOR, text_bg_color=TEXT_BG_COLOR,
                 text_font_name=None, accent_color=ACCENT_COLOR,
                 line_thickness=LINE_THICKNESS):
        super().__init__()

        pygame.init()
        self._screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
        self._bg_color = bg_color
        self._line_color = line_color
        self._accent_color = accent_color  # for least cost path and the rect surrounding the icons
        self._line_thickness = line_thickness
        self._graph = graph
        self._md = md
        self._text_color = text_color
        self._text_bg_color = text_bg_color
        self._text_font = pygame.font.SysFont(text_font_name, INFO_HEIGHT)
        self._path = []  # for least cost path between 2 vertices
        self._edges = []
        self._vertices = []
        self._vertices_count = None
        self._side_count = None
        self._tile_width = None
        self._tile_height = None
        self._hover_vertex = None
        self._start_vertex = None
        self._end_vertex = None
        self.update(graph, md)

    def update(self, graph, md):
        """
        call this method to inform the GUI about the Graph and meta-data change
        """
        self._graph = graph
        self._md = md
        if graph is None:
            return

        self._edges = graph.edges()  # call once and be done
        self._vertices = graph.vertices()  # call once and be done

        self._vertices_count = len(self._vertices)  # call once and be done

        # we're making a big square grid, there will be side_count * side_count tiles
        # example: given: 4 vertices; need: 2x2 grid; side_count = ceil(sqrt(4)) = 2
        # example: given: 5 vertices; need: 3x3 grid; side_count = ceil(sqrt(5)) = 3
        self._side_count = math.ceil(math.sqrt(self._vertices_count))

        # making tiles for each icon
        self._tile_width = GRAPH_WIDTH / self._side_count
        self._tile_height = GRAPH_HEIGHT / self._side_count

        for index, vertex in enumerate(self._vertices):
            # magic. x_start and y_start defines the starting position for a tile

            # x: index % side_count will always evaluate to (0, 1, 2, side_count - 1)
            # x: index will keep incrementing, and return to 0 when a new line is formed

            # y: index // side_count will always evaluate to (0, 1, 2, side_count - 1)
            # y: index will not increment until the end of line is reached

            x_start = self._tile_width * (index % self._side_count)
            y_start = self._tile_height * (index // self._side_count)

            # random positioning of the icon in the tile
            x_pos = x_start + random.randrange(0, self._tile_width - IMG_WIDTH)
            y_pos = y_start + random.randrange(0, self._tile_height - IMG_HEIGHT)

            # store the position in the meta-data
            self._set_img_position_for(vertex, (x_pos, y_pos))

    def _update_path(self):
        """
        call only when start_vertex and end_vertex are both not None
        """
        # cost is the same for each edge, therefore, lambda e: 1
        vertices = least_cost_path(self._graph, self._start_vertex, self._end_vertex, lambda e: 1)
        if len(vertices) <= 0:
            # no path? reset the UI to accept new input
            self._clear_path()
            return

        # we need a collection of edges for drawing a different colour
        self._path = vertices_to_edges(vertices)

        self.draw()  # update the UI

    def _clear_path(self):
        self._start_vertex = None
        self._end_vertex = None
        self._path = []
        self.draw()  # update the UI

    def on_click(self, event):
        if event.button == 1:  # magic number from pygame
            self._on_left_click()
        elif event.button == 3:  # magic number from pygame
            self._on_right_click()

    def _on_left_click(self):
        # left click triggers path finding mechanism
        if self._start_vertex is not None and self._end_vertex is not None:
            self._clear_path()  # clicking when a path is active? OK, you're done with the path
        if self._hover_vertex is not None:  # clicked on an icon
            if self._start_vertex is None:  # a fresh start!
                self._start_vertex = self._hover_vertex
                self.draw_vertex(self._start_vertex)  # this will outline the icon with the accent colour
            else:  # one step closer to success!
                self._end_vertex = self._hover_vertex
                self.draw_vertex(self._end_vertex)  # this will outline the icon with the accent colour
                self._update_path()  # summon the path!
        else:  # clicking randomly on screen? OK, you're done with the path
            self._clear_path()

    def _on_right_click(self):
        if self._hover_vertex is not None:
            webbrowser.open_new_tab(self._hover_vertex)  # boom, going back in history
        else:  # clicking randomly on screen? OK, you're done with the path
            self._clear_path()

    def on_move(self, event):
        x, y = event.pos
        x_index = x // self._tile_width  # the tile x-index
        y_index = y // self._tile_height  # the tile y-index

        vertex_index = int(x_index + self._side_count * y_index)  # the index in our list
        if vertex_index >= self._vertices_count:  # mouse is pointing at nothing (remember we need 9 tiles for 5 icons?)
            self._hover_vertex = None
            return  # kthxbye

        vertex = self._vertices[vertex_index]  # find the icon
        x_start, y_start = self._get_img_position_from(vertex)  # see where it is

        if x_start <= x <= x_start + IMG_WIDTH \
                and y_start <= y <= y_start + IMG_HEIGHT:  # is the mouse on it?
            self._hover_vertex = vertex
        else:
            self._hover_vertex = None

        self.draw_info_box()  # update the text (show website title, or just default prompt)

    def draw_vertex(self, vertex):
        """
        draws an icon on screen, the vertex must be a key in the meta-data dict
        it will be outlined if the vertex is start_vertex or end_vertex
        """
        # the icon file location
        img_path = 'images/default.png' if vertex is None else self._get_img_path_from(vertex)
        icon = pygame.image.load(img_path)
        # EVERYONE SHALL OBEY THE IMAGE SIZE
        icon = pygame.transform.scale(icon, (IMG_WIDTH, IMG_HEIGHT))
        # where to draw?
        pos = self._get_img_position_from(vertex)

        if vertex == self._start_vertex or vertex == self._end_vertex:
            # you are the chosen one, I'll put a ring on you
            outline = (pos[0], pos[1], icon.get_width(), icon.get_height())
            pygame.draw.rect(self._screen, self._accent_color, outline, 2)

        # blast that thing on screen
        self._screen.blit(icon, pos)
        pygame.display.flip()

    def draw_edge(self, edge):
        """
        draws an edge on screen, both vertices must be keys in the meta-data dict
        the line will be in accent colour if it is part of the path
        """
        # from where? to where?
        start_x, start_y, end_x, end_y = self._points_for_lines_from_edge(edge)

        # are you the one?
        if edge in self._path or (edge[1], edge[0]) in self._path:  # check the reverse path so colours don't overlap
            color = self._accent_color
        else:
            color = self._line_color

        start = (start_x, start_y)
        end = (end_x, end_y)

        # let's do this
        pygame.draw.aaline(self._screen, color, start, end, self._line_thickness)
        pygame.display.flip()

    def _draw_end_point_indicator(self, edge):
        """
        draws an end point indicator at the 75% position of the edge (closer to the end)
        (so basically, bisect twice, an place the indicator closer to the end)
        """
        # from where? to where?
        start_x, start_y, end_x, end_y = self._points_for_lines_from_edge(edge)

        # 50%
        mid_x, mid_y = mid_point(start_x, start_y, end_x, end_y)  # +start *mid +end +-----*-----+
        # 75%
        mid_end_x, mid_end_y = mid_point(mid_x, mid_y, end_x, end_y)  # +start +old_mid *mid +end +-----+--*--+

        # the circle function wants all int for some reason
        x = round(mid_end_x)
        y = round(mid_end_y)

        # a dot, how cool
        pygame.draw.circle(self._screen, self._accent_color, (x, y), int(self._line_thickness * 2))
        pygame.display.flip()

    def draw_info_box(self):
        """
        draws the background and the info text on screen.
        displays the link title if the mouse is hovering on an icon, shows the default prompt otherwise
        """
        text = INFO_PROMPT if self._hover_vertex is None else self._get_page_title_from(self._hover_vertex)

        # draw the text background
        text_bg_rect = (0, TOTAL_HEIGHT - INFO_HEIGHT, INFO_WIDTH, INFO_HEIGHT)
        pygame.draw.rect(self._screen, self._text_bg_color, text_bg_rect)

        # gimme the text!
        text = self._text_font.render(text, True, self._text_color)

        # the height element of size
        text_height = text.get_size()[1]
        # vertical centering
        pos_y_in_box = (INFO_HEIGHT - text_height) / 2

        # draw there!
        text_pos = (0, TOTAL_HEIGHT - INFO_HEIGHT + pos_y_in_box)

        # word is the most powerful weapon
        self._screen.blit(text, text_pos)
        pygame.display.flip()

    def draw(self):
        """
        draws everything on screen
        order (bottom to top): background -> edges -> end point indicator -> icons -> info box
        """
        self._screen.fill(self._bg_color)

        for edge in self._edges:  # draw the lines first
            self.draw_edge(edge)

        for edge in self._edges:  # have to loop again to avoid lines overdrawing the indicators
            self._draw_end_point_indicator(edge)

        for vertex in self._vertices:  # draw the icons
            self.draw_vertex(vertex)

        self.draw_info_box()  # draw the info text

    def _points_for_lines_from_edge(self, edge):
        """
        returns start_x, start_y, end_x, end_y to draw a line
        from the center of the start icon to the center of the end icon
        """
        pos_start = self._get_img_position_from(edge[0])
        start_x, start_y = pos_start[0], pos_start[1]  # top-left corner

        start_x += IMG_WIDTH / 2
        start_y += IMG_HEIGHT / 2

        pos_end = self._get_img_position_from(edge[1])
        end_x, end_y = pos_end[0], pos_end[1]  # top-left corner

        end_x += IMG_WIDTH / 2
        end_y += IMG_HEIGHT / 2

        return start_x, start_y, end_x, end_y

    ### one-liner functions. why? +readability +avoid magic numbers +painless refactoring

    def _get_page_title_from(self, vertex):
        """
        returns the page title from the link
        """
        return self._md[vertex][0]

    def _get_img_path_from(self, vertex):
        """
        returns the image file location from the link
        """
        return self._md[vertex][1]

    def _get_img_position_from(self, vertex):
        """
        returns the top-left corner of the image position from the link
        """
        return self._md[vertex][2]

    def _set_img_position_for(self, vertex, pos):
        """
        stores the top-left corner of the image position for the link
        """
        self._md[vertex][2] = pos


def vertices_to_edges(vertices):
    """
    takes a list of vertices which length is >= 2, return a list of tuple pairs of edges
    """
    length = len(vertices)
    if length <= 1:
        return vertices  # stop trolling, you call a list of a vertex a path?
    edges = []
    last = vertices[0]  # let's begin with the 1st element
    for vertex in vertices[1:]:  # we loop from the 2nd element, since we started with the 1st
        edges.append((last, vertex))
        last = vertex
    return edges


def mid_point(start_x, start_y, end_x, end_y):
    """
    returns the mid point of two points
    """
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    return mid_x, mid_y