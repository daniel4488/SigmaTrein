from .map import PlotlyLoad
from code.classes.solution import Solution
from code.classes.output import Output
from code.visualisation.baseline import visualize_iterations_to_score


class MapVisualization:
    """
    Class used to create the visualistation of a solution.
    """

    def create_visual(self, solution: Solution, path: str, auto_open: bool):
        Output(solution.trajectories, True)
        visualize_iterations_to_score(data=path, auto_open=auto_open)
        self.visualize(solution=solution, auto_open=auto_open)

    def visualize(self, solution: Solution, auto_open: bool):
        assert hasattr(self, "dataset")
        plot_device = PlotlyLoad(dataset=self.dataset)
        plot_device.draw_graph(solution, auto_open=auto_open)
