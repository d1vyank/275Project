import random
import math
import webbrowser

import pygame

from graph import least_cost_path


IMG_WIDTH = 32
IMG_HEIGHT = IMG_WIDTH

GRAPH_WIDTH = 800
GRAPH_HEIGHT = GRAPH_WIDTH

INFO_WIDTH = GRAPH_WIDTH
INFO_HEIGHT = 30

TOTAL_WIDTH = GRAPH_WIDTH
TOTAL_HEIGHT = GRAPH_HEIGHT + INFO_HEIGHT

LINE_THICKNESS = 1
INFO_PROMPT = "Hover: view link; left click: launch link in browser; right click: least cost path."

ARROW_LENGTH = 30


class Gui:
    def __init__(self, graph, md, bg_color, line_color, text_color,
                 text_bg_color, text_font_name=None, accent_color=(0, 255, 0),
                 arrow_length=ARROW_LENGTH, line_thickness=LINE_THICKNESS):
        super().__init__()

        pygame.init()
        self._screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
        self._bg_color = bg_color
        self._line_color = line_color
        self._accent_color = accent_color  # for least cost path and the rect surrounding the icons
        self._arrow_length = arrow_length
        self._line_thickness = line_thickness
        self._graph = graph
        self._md = md
        self._text_color = text_color
        self._text_bg_color = text_bg_color
        self._text_font = pygame.font.SysFont(text_font_name, INFO_HEIGHT)
        self._edges = []
        self._path = []  # for least cost path between 2 vertices
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
        self._graph = graph
        self._md = md
        if graph is None:
            return
        self._edges = graph.edges()
        self._vertices = graph.vertices()

        self._vertices_count = len(self._vertices)
        self._side_count = math.ceil(math.sqrt(self._vertices_count) + 0.5)

        self._tile_width = GRAPH_WIDTH / self._side_count
        self._tile_height = GRAPH_HEIGHT / self._side_count

        for index, vertex in enumerate(self._vertices):
            x_start = self._tile_width * (index % self._side_count)
            y_start = self._tile_height * (index // self._side_count)

            x_pos = x_start + random.randrange(0, self._tile_width - IMG_WIDTH)
            y_pos = y_start + random.randrange(0,
                                               self._tile_height - IMG_HEIGHT)
            self._set_img_position_for(vertex, (x_pos, y_pos))

    def _update_path(self):
        vertices = least_cost_path(self._graph, self._start_vertex, self._end_vertex, lambda e: 1)
        if len(vertices) <= 0:
            self._clear_path()
            return

        self._path = vertices_to_edges(vertices)

        self.draw()

    def _clear_path(self):
        self._start_vertex = None
        self._end_vertex = None
        self._path = []
        self.draw()

    def on_click(self, event):
        if event.button == 1:
            self._on_left_click()
        elif event.button == 3:
            self._on_right_click()

    def _on_left_click(self):
        if self._hover_vertex is not None:
            webbrowser.open_new_tab(self._hover_vertex)
        else:
            self._clear_path()

    def _on_right_click(self):
        if self._start_vertex is not None and self._end_vertex is not None:
            self._clear_path()
        if self._hover_vertex is not None:
            if self._start_vertex is None:
                self._start_vertex = self._hover_vertex
                self.draw_vertex(self._start_vertex)
            else:
                self._end_vertex = self._hover_vertex
                self.draw_vertex(self._start_vertex)
                self._update_path()
        else:
            self._clear_path()

    def on_move(self, event):
        x, y = event.pos
        x_index = x // self._tile_width
        y_index = y // self._tile_height

        vertex_index = int(x_index + self._side_count * y_index)
        if vertex_index >= self._vertices_count:
            self._hover_vertex = None
            return

        vertex = self._vertices[vertex_index]
        x_start, y_start = self._get_img_position_from(vertex)

        if x_start <= x <= x_start + IMG_WIDTH \
                and y_start <= y <= y_start + IMG_HEIGHT:
            self._hover_vertex = vertex
        else:
            self._hover_vertex = None

        self.draw_info_box()

    def draw_vertex(self, vertex):
        img_path = 'images/default.png' if vertex is None else self._get_img_path_from(vertex)
        icon = pygame.image.load(img_path)
        icon = pygame.transform.scale(icon, (IMG_WIDTH, IMG_HEIGHT))
        pos = self._get_img_position_from(vertex)

        if vertex == self._start_vertex or vertex == self._end_vertex:
            outline = (pos[0], pos[1], icon.get_width(), icon.get_height())
            pygame.draw.rect(self._screen, self._accent_color, outline, 2)

        self._screen.blit(icon, pos)
        pygame.display.flip()

    def draw_edge(self, edge):
        start_x, start_y = self._get_img_position_from(edge[0])
        start_x += IMG_WIDTH / 2
        start_y += IMG_HEIGHT / 2
        start = (start_x, start_y)

        end_x, end_y = self._get_img_position_from(edge[1])
        end_x += IMG_WIDTH / 2
        end_y += IMG_HEIGHT / 2
        end = (end_x, end_y)

        if edge in self._path or (edge[1], edge[0]) in self._path:  # check the reverse path so colours don't overlap
            color = self._accent_color
        else:
            color = self._line_color

        pygame.draw.aaline(self._screen, color, start, end, self._line_thickness)
        pygame.display.flip()

    def draw_info_box(self):
        text = INFO_PROMPT if self._hover_vertex is None else self._hover_vertex

        text_bg_rect = (0, TOTAL_HEIGHT - INFO_HEIGHT, INFO_WIDTH, INFO_HEIGHT)
        pygame.draw.rect(self._screen, self._text_bg_color, text_bg_rect)

        text = self._text_font.render(text, True, self._text_color)

        text_height = text.get_size()[1]
        pos_y_in_box = (INFO_HEIGHT - text_height) / 2

        text_pos = (0, TOTAL_HEIGHT - INFO_HEIGHT + pos_y_in_box)

        self._screen.blit(text, text_pos)
        pygame.display.flip()

    def draw(self):
        self._screen.fill(self._bg_color)

        for edge in self._edges:
            self.draw_edge(edge)

        for vertex in self._vertices:
            self.draw_vertex(vertex)

        self.draw_info_box()

    def _get_img_path_from(self, vertex):
        return self._md[vertex][1]

    def _get_img_position_from(self, vertex):
        return self._md[vertex][2]

    def _set_img_position_for(self, vertex, pos):
        self._md[vertex][2] = pos


def vertices_to_edges(vertices):
    length = len(vertices)
    if length <= 1:
        return vertices
    # if length == 2:
    #     return [(vertices[0], vertices[1])]
    edges = []
    last = vertices[0]
    for vertex in vertices[1:]:
        edges.append((last, vertex))
        last = vertex
    return edges