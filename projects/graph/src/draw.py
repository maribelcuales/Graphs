"""
General drawing methods for graphs using Bokeh.
"""

from random import choice, random
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import (GraphRenderer, StaticLayoutProvider, Circle, LabelSet,
                          ColumnDataSource)


class BokehGraph:
    """Class that takes a graph and exposes drawing methods."""
    def __init__(self, graph, title="Graph", width=10, height=10, 
                show_axis=False, show_grid=False, circle_size=35):
        
        if not graph.vertices:
            raise Exception('Graph should contain vertices!')
        self.graph = graph

        #Setup plot
        self.width = width
        self.height = height
        self.pos = {} # dict to map vertices to x, y positions
        self.plot = figure(title=title, x_range=(0, width), y_range=(0, height))
        self.plot.axis.visible = show_axis
        self.plot.grid.visible = show_grid
        self._setup_graph_renderer(circle_size)
        self._setup_labels()
    
    def _setup_graph_renderer(self, circle_size):
        graph_renderer = GraphRenderer()

        graph_renderer.node_renderer.data_source.add(
            list(self.graph.vertices.keys()), 'index')
        graph_renderer.node_renderer.data_source.add(
            self._get_random_colors(), 'color')
        graph_renderer.node_renderer.glyph = Circle(size=circle_size, fill_color='color')
        graph_renderer.edge_renderer.data_source.data = self._get_edge_indexes()
        self.randomize()
        graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=self.pos)
        self.plot.renderers.append(graph_renderer)

    def _get_random_colors(self):
        colors = []
        for _ in range(len(self.graph.vertices)):
            color = '#'+''.join([choice('0123456789ABCDEF') for j in range(6)])
            colors.append(color)
        return colors

    def _get_edge_indexes(self):
        start_indices = []
        end_indices = []
        checked = set()

        for vertex, edges in self.graph.vertices.items():
            if vertex not in checked:
                for destination in edges:
                    start_indices.append(vertex)
                    end_indices.append(destination)
                checked.add(vertex)
        
        return dict(start=start_indices, end=end_indices)

    def _setup_labels(self):
        label_data = {'x': [], 'y':[], 'names':[]}
        for vertex, position in self.pos.items():
            label_data['x'].append(position[0])
            label_data['y'].append(position[1])
            label_data['names'].append(str(vertex))
        label_source = ColumnDataSource(label_data)
        labels = LabelSet(x='x', y='y', text='names', level='glyph', 
                        text_align='center', text_baseline='middle', 
                        source=label_source, render_mode='canvas')
        self.plot.add_layout(labels)
    
    def show(self, output_path='./graph.html'):
        output_file(output_path)
        show(self.plot)

    def randomize(self):
        """Randomize vertex positions"""
        for vertex in self.graph.vertices:
            # TODO make bounds and random draws less hacky
            self.pos[vertex] = (1 + random() * (self.width - 2),
                                1 + random() * (self.height - 2))

from graph import Graph
from draw import BokehGraph

graph = Graph()
graph.add_vertex("0")
graph.add_vertex("1")
graph.add_vertex("2")
graph.add_vertex("3")
graph.add_vertex("4")
graph.add_vertex("5")
graph.add_vertex("6")
graph.add_vertex("7")
graph.add_vertex("8")
graph.add_vertex("9")
graph.add_vertex("10")
graph.add_vertex("11")
graph.add_vertex("12")
graph.add_vertex("13")
graph.add_vertex("14")
graph.add_vertex("15")
graph.add_vertex("16")
graph.add_vertex("17")
graph.add_vertex("18")
graph.add_vertex("19")

graph.add_edge("1", "2")
graph.add_edge("2", "7")
graph.add_edge("7", "6")
graph.add_edge("5", "6")
graph.add_edge("5", "10")
graph.add_edge("3", "8")
graph.add_edge("7", "6")
graph.add_edge("8", "7")
graph.add_edge("8", "13")
graph.add_edge("8", "9")
graph.add_edge("9", "14")
graph.add_edge("12", "13")
graph.add_edge("13", "14")
graph.add_edge("15", "16")
graph.add_edge("16", "17")

graph.vertices

bg = BokehGraph(graph)
dir(bg)
bg.pos
bg.plot
bg.show()
graph

# g = Graph()
# g.randomize(5, 4, 150, 0.6)