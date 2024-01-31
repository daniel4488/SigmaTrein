from .map import PlotlyLoad
from code.classes.solution import Solution


class MapVisualization:

    def visualize(self, solution: Solution, auto_open: bool):
        assert hasattr(self, "dataset")
        plot_device = PlotlyLoad(dataset=self.dataset)
        plot_device.draw_graph(solution, auto_open=auto_open)
