import random
import pygame
import math
import webbrowser

IMG_WIDTH = 32
IMG_HEIGHT = IMG_WIDTH

GRAPH_WIDTH = 800
GRAPH_HEIGHT = GRAPH_WIDTH

INFO_WIDTH = GRAPH_WIDTH
INFO_HEIGHT = 30

TOTAL_WIDTH = GRAPH_WIDTH
TOTAL_HEIGHT = GRAPH_HEIGHT + INFO_HEIGHT

LINE_THICKNESS = 1
INFO_PROMPT = "Hover to view link. Click to launch in browser."


class Gui:
    def __init__(self, graph, md, bg_color, line_color, text_color, text_bg_color, text_font_name=None):
        super().__init__()

        pygame.init()
        self._screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
        self._bg_color = bg_color
        self._line_color = line_color
        self._graph = graph
        self._md = md
        self._text_color = text_color
        self._text_bg_color = text_bg_color
        self._text_font = pygame.font.SysFont(text_font_name, INFO_HEIGHT)
        self._edges = None
        self._vertices = None
        self._vertices_count = None
        self._side_count = None
        self._tile_width = None
        self._tile_height = None
        self._hover_vertex = None
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

        for index, value in enumerate(self._vertices):
            x_start = self._tile_width * (index % self._side_count)
            y_start = self._tile_height * (index // self._side_count)

            x_pos = x_start + random.randrange(0, self._tile_width - IMG_WIDTH)
            y_pos = y_start + random.randrange(0, self._tile_height - IMG_HEIGHT)
            self._md[value][2] = (x_pos, y_pos)

    def draw(self):
        self._screen.fill(self._bg_color)

        for edge in self._edges:
            self.draw_edge(edge)

        for value in self._vertices:
            meta_data = self._md[value]
            image_path = meta_data[1]
            self.draw_icon(image_path, meta_data[2])

        self.draw_hover_vertex()

        pygame.display.flip()

    def on_click(self, event):
        if self._hover_vertex is not None:
            webbrowser.open_new_tab(self._hover_vertex)

    def on_move(self, event):
        x, y = event.pos
        x_index = x // self._tile_width
        y_index = y // self._tile_height

        vertex_index = int(x_index + self._side_count * y_index)
        if vertex_index >= self._vertices_count:
            self._hover_vertex = None
            return

        vertex = self._vertices[vertex_index]
        x_start, y_start = self._md[vertex][2]

        if x_start <= x <= x_start + IMG_WIDTH and \
                                y_start <= y <= y_start + IMG_HEIGHT:
            self._hover_vertex = vertex
        else:
            self._hover_vertex = None

        self.draw()

    def draw_icon(self, img_path, pos):
        img_path = 'images/default.png' if img_path is None else img_path
        icon = pygame.image.load(img_path)
        icon = pygame.transform.scale(icon, (IMG_WIDTH, IMG_HEIGHT))
        self._screen.blit(icon, pos)

    def draw_edge(self, edge):
        start_x, start_y = self._md[edge[0]][2]
        start_x += IMG_WIDTH / 2
        start_y += IMG_HEIGHT / 2
        start = (start_x, start_y)

        end_x, end_y = self._md[edge[1]][2]
        end_x += IMG_WIDTH / 2
        end_y += IMG_HEIGHT / 2
        end = (end_x, end_y)

        pygame.draw.lines(self._screen, self._line_color, False, [start, end], LINE_THICKNESS)

    def draw_hover_vertex(self):
        text = INFO_PROMPT if self._hover_vertex is None else self._hover_vertex

        text_bg_rect = (0, TOTAL_HEIGHT - INFO_HEIGHT, INFO_WIDTH, INFO_HEIGHT)
        pygame.draw.rect(self._screen, self._text_bg_color, text_bg_rect)

        text = self._text_font.render(text, True, self._text_color)

        text_height = text.get_size()[1]
        pos_y_in_box = (INFO_HEIGHT - text_height) / 2

        text_pos = (0, TOTAL_HEIGHT - INFO_HEIGHT + pos_y_in_box)

        self._screen.blit(text, text_pos)