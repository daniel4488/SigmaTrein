from code.visualisation.load import Load
from code.classes.solution import Solution
from code.classes.output import Output

import plotly.graph_objects as go
import numpy as np
import os


class PlotlyLoad(Load):
    def __init__(self, dataset: str) -> None:
        super().__init__(dataset=dataset)

        # mapbox token
        self.token = open("code/visualisation/.mapbox_token").read()

        self.coloring: list[str] = [
            "#ffffff", "#ff0000", "#00ff00", "#0000ff", "#ff00ff",
            "#00ffff", "#ffff00", "#ff8000", "#80ff00", "#0080ff",
            "#ff0080", "#80ffff", "#ff80ff", "#ffff80", "#ffbf00",
            "#40ff00", "#0040ff", "#ff0040", "#40ffff", "#ffbf80"
        ]
        self.edges: dict[tuple[str, str], list[str]] = {}

        self.verbose: bool = False

    def draw_graph(self, solution: Solution | Output, auto_open: bool) -> None:

        traject_total_time = 0

        # create edges
        edge_traces_gray = []
        middle_node_x = []
        middle_node_y = []
        middle_node_text = []

        for edge in self.G.edges():
            edge_trace = go.Scattermapbox(
                lon=[], lat=[],
                line=dict(
                    width=1,
                    color='#888'
                ),
                hoverinfo='none',
                mode='lines'
            )

            x0 = self.G.nodes[edge[0]]['x']
            y0 = self.G.nodes[edge[0]]['y']
            x1 = self.G.nodes[edge[1]]['x']
            y1 = self.G.nodes[edge[1]]['y']

            edge_trace["lon"] += (x0, x1, None)
            edge_trace["lat"] += (y0, y1, None)
            edge_traces_gray.append(edge_trace)

            middle_node_x.append((x0 + x1) / 2)
            middle_node_y.append((y0 + y1) / 2)
            middle_node_text.append(self.G.edges[edge]['title'])

        for traject_number, traject in enumerate(solution.trajectories):
            stations = traject.stations
            edges = list(map(lambda x: tuple(sorted(x)), zip(stations, stations[1:])))
            for edge in edges:
                if edge in self.edges:
                    self.edges[edge].append(self.coloring[traject_number])
                else:
                    self.edges[edge] = [self.coloring[traject_number]]

        edge_traces = []
        for edge, trajectory_colors in self.edges.items():
            print(edge) if self.verbose else None
            if len(trajectory_colors) == 1:
                edge_trace = go.Scattermapbox(
                    lon=[], lat=[],
                    line=dict(
                        width=2,
                        color=trajectory_colors[0]
                    ),
                    hoverinfo='none',
                    mode='lines'
                )

                x0 = self.G.nodes[edge[0]]['x']
                y0 = self.G.nodes[edge[0]]['y']
                x1 = self.G.nodes[edge[1]]['x']
                y1 = self.G.nodes[edge[1]]['y']

                edge_trace["lon"] += (x0, x1, None)
                edge_trace["lat"] += (y0, y1, None)
                edge_traces.append(edge_trace)
            else:
                for double_edge_count, trajectory_color in enumerate(trajectory_colors):
                    edge_trace = go.Scattermapbox(
                        lon=[], lat=[],
                        line=dict(
                            width=2,
                            color=trajectory_color
                        ),
                        hoverinfo='none',
                        mode='lines'
                    )
                    x0 = self.G.nodes[edge[0]]['x']
                    y0 = self.G.nodes[edge[0]]['y']
                    x1 = self.G.nodes[edge[1]]['x']
                    y1 = self.G.nodes[edge[1]]['y']

                    source_vector = np.array([x0, y0], dtype=np.double)
                    destination_vector = np.array([x1, y1], dtype=np.double)

                    original_vector = np.array([x1 - x0, y1 - y0], dtype=np.double)
                    rotation_matrix = (-1) ** double_edge_count * np.array([[0, -1], [1, 0]])
                    orthogonal_vector = np.matmul(original_vector, rotation_matrix)

                    assert np.dot(original_vector, orthogonal_vector) < 1e-12
                    orthogonal_vector /= np.linalg.norm(orthogonal_vector)  # normalize it
                    assert np.linalg.norm(orthogonal_vector) - 1.0 < 1e-12

                    source_vector += orthogonal_vector * 0.004 * double_edge_count
                    destination_vector += orthogonal_vector * 0.004 * double_edge_count
                    print(f"source vector: {source_vector}") if self.verbose else None
                    print(f"destination vector: {destination_vector}") if self.verbose else None

                    x0 = source_vector[0]
                    y0 = source_vector[1]
                    x1 = destination_vector[0]
                    y1 = destination_vector[1]

                    edge_trace["lon"] += (x0, x1, None)
                    edge_trace["lat"] += (y0, y1, None)
                    edge_traces.append(edge_trace)

        # Distance label of edges
        middle_node_trace = go.Scattermapbox(
            lon=middle_node_x, lat=middle_node_y,
            mode='markers+text',
            hoverinfo='none',
            marker=dict(
                color='#888',
                size=15
            ),
            text=middle_node_text,
            textposition='middle center',
            textfont=dict(
                size=8,
                color="#ffffff"
            )
        )

        node_x = []
        node_y = []
        city_name = []
        for node in self.G.nodes():
            x = self.G.nodes[node]['x']
            y = self.G.nodes[node]['y']
            node_x.append(x)
            node_y.append(y)
            city_name.append(node)

        node_trace = go.Scattermapbox(
            lon=node_x, lat=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                color='LightSkyBlue',
                size=10,
            ),
            text=city_name,
            textposition='bottom center',
        )

        # create network graph
        fig = go.Figure(
            data=[*edge_traces_gray, *edge_traces, node_trace, middle_node_trace],
            layout=go.Layout(
                title='Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(l=0, r=0, t=0, b=0),
                annotations=[dict(
                    text="RailNL",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002)],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleratio=1),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleratio=1),
                plot_bgcolor="white",
                paper_bgcolor="#ECEEFE",
            )
        )

        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    active=0,
                    x=0.57,
                    y=1.2,
                    buttons=list(
                        [
                            dict(
                                label="Show distance",
                                method="update",
                                args=[
                                    {
                                        "visible": [True]
                                    }
                                ]
                            ),
                            dict(
                                label="Hide distance",
                                method="update",
                                args=[
                                    {
                                        "visible": [True] * (len(fig.data) - 1) + [False]
                                    }
                                ]
                            )
                        ]
                    )
                )
            ]
        )

        # Add track info
        fig.add_annotation(
            text=f"<b>Traject:</b> [traject] <br><b>Total time:</b> {traject_total_time}",
            align="left",
            xref="paper",
            yref="paper",
            showarrow=False,
            x=0,
            y=-0.1
        )

        # Map settings
        fig.update_layout(mapbox_accesstoken=self.token)
        fig.update_layout(mapbox_style="mapbox://styles/daniel181/clrooylos004201pedtslc1km")
        fig.update_layout(
            mapbox={
                "center": {
                    "lon": 5.6464,
                    "lat": 52.1006
                },
                "zoom": 6.3
            }
        )

        if not os.path.exists(".tmp"):
            os.mkdir(".tmp")
        fig.write_html(".tmp/single_track.html", auto_open=auto_open)
