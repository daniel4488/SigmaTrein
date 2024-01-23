# from load import Load
from code.visualisation.load import Load
import plotly.graph_objects as go
import os


class PlotlyLoad(Load):
    def __init__(self) -> None:
        super().__init__(dataset="holland")

    def draw_graph(self, trajectory: list[str]) -> None:

        # attr = {
        #     "distance": 2,
        #     "title": "2"
        # }
        # self.G.add_edge("Den Helder", "Alkmaar", **attr)

        # trajectory
        # trajectory = ["Beverwijk", "Castricum", "Alkmaar", "Hoorn", "Zaandam"]
        trajectory_edges = set((trajectory[i], trajectory[i + 1]) for i in range(len(trajectory) - 1))
        trajectory_total_time = 0

        # # create edges
        # edge_x = []
        # edge_y = []
        # middle_node_x = []
        # middle_node_y = []
        # middle_node_text = []
        # for edge in self.G.edges():
        #     x0 = self.G.nodes[edge[0]]['x']
        #     y0 = self.G.nodes[edge[0]]['y']
        #     x1 = self.G.nodes[edge[1]]['x']
        #     y1 = self.G.nodes[edge[1]]['y']
        #     edge_x.append(x0)
        #     edge_x.append(x1)
        #     edge_x.append(None)
        #     edge_y.append(y0)
        #     edge_y.append(y1)
        #     edge_y.append(None)
        #     middle_node_x.append((x0 + x1) / 2)
        #     middle_node_y.append((y0 + y1) / 2)
        #     middle_node_text.append(self.G.edges[edge]['title'])
        #
        # edge_trace = go.Scatter(
        #     x=edge_x, y=edge_y,
        #     line=dict(width=0.5, color='#888'),
        #     hoverinfo='none',
        #     mode='lines'
        # )

        # create edges
        edge_traces = []
        middle_node_x = []
        middle_node_y = []
        middle_node_text = []
        for edge in self.G.edges():
            if edge in trajectory_edges or (edge[1], edge[0]) in trajectory_edges:
                edge_trace = go.Scatter(
                    x=[], y=[],
                    line=dict(
                        width=2,
                        color="#ce2d4f"
                    ),
                    hoverinfo='none',
                    mode='lines'
                )
                trajectory_total_time += self.G.edges[edge]["distance"]
            else:
                # color = '#888'
                edge_trace = go.Scatter(
                    x=[], y=[],
                    line=dict(
                        width=1,
                        color='#888'
                    ),
                    hoverinfo='none',
                    mode='lines'
                )

            # edge_trace = go.Scatter(
            #     x=[], y=[],
            #     line=dict(
            #         width=1,
            #         color=color
            #     ),
            #     hoverinfo='none',
            #     mode='lines'
            # )

            x0 = self.G.nodes[edge[0]]['x']
            y0 = self.G.nodes[edge[0]]['y']
            x1 = self.G.nodes[edge[1]]['x']
            y1 = self.G.nodes[edge[1]]['y']

            edge_trace["x"] += (x0, x1, None)
            edge_trace["y"] += (y0, y1, None)
            edge_traces.append(edge_trace)

            middle_node_x.append((x0 + x1) / 2)
            middle_node_y.append((y0 + y1) / 2)
            middle_node_text.append(self.G.edges[edge]['title'])

        # edge_trace = go.Scatter(
        #     x=edge_x, y=edge_y,
        #     line=dict(width=0.5, color='#888'),
        #     hoverinfo='none',
        #     mode='lines'
        # )

        middle_node_trace = go.Scatter(
            x=middle_node_x, y=middle_node_y,
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

        # # trajectory
        # trajectory = ["Beverwijk", "Castricum", "Alkmaar", "Hoorn", "Zaandam"]
        #
        # trajectory_edge_x = []
        # trajectory_edge_y = []
        #
        # for edge in iter.combinations(trajectory, r=2):
        #     x0 = self.G.nodes[edge[0]]['x']
        #     y0 = self.G.nodes[edge[0]]['y']
        #     x1 = self.G.nodes[edge[1]]['x']
        #     y1 = self.G.nodes[edge[1]]['y']
        #     trajectory_edge_x.append(x0)
        #     trajectory_edge_x.append(x1)
        #     trajectory_edge_x.append(None)
        #     trajectory_edge_y.append(y0)
        #     trajectory_edge_y.append(y1)
        #     trajectory_edge_y.append(None)
        #
        # trajectory_trace = go.Scatter(
        #     x=trajectory_edge_x, y=trajectory_edge_y,
        #     line=dict(width=0.5, color='lightgreen'),
        #     hoverinfo='none',
        #     mode='lines'
        # )

        node_x = []
        node_y = []
        city_name = []
        for node in self.G.nodes():
            x = self.G.nodes[node]['x']
            y = self.G.nodes[node]['y']
            node_x.append(x)
            node_y.append(y)
            city_name.append(node)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                # showscale=True,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                # colorscale='YlGnBu',
                # reversescale=True,
                # color=[],
                color='LightSkyBlue',
                size=10,
                # colorbar=dict(
                #     thickness=15,
                #     title='Node Connections',
                #     xanchor='left',
                #     titleside='right'
                # ),
                line=dict(
                    width=1,
                    color="RoyalBlue"
                )
            ),
            text=city_name,
            textposition='bottom center'
        )

        # # color node points
        # node_adjacencies = []
        # node_text = []
        # for node, adjacencies in enumerate(self.G.adjacency()):
        #     node_adjacencies.append(len(adjacencies[1]))
        #     node_text.append('# of connections: ' + str(len(adjacencies[1])))
        #
        # node_trace.marker.color = node_adjacencies
        # node_trace.text = node_text

        # button = list(
        #     dict(
        #         method="update",
        #         label="Label",
        #         visible=True,
        #         args=list(
        #             {
        #                 "visible": [True] * len(edge_traces) + [True, False]
        #             }
        #         )
        #     )
        # )

        # create network graph
        fig = go.Figure(data=[*edge_traces, node_trace, middle_node_trace],
                        layout=go.Layout(
                            title='Network graph made with Python',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            # margin=dict(b=20, l=5, r=5, t=40),
                            # autosize=False,
                            # width=800,
                            # height=800,
                            margin=dict(pad=4),
                            annotations=[dict(
                                text="RailNL",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleratio=1),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleratio=2),
                            # xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleratio=1, range=[2.314634, 6.041746]),
                            # yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleratio=2, range=[51.754184, 53.007841]),
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
            text=f"<b>Trajectory:</b> {trajectory}<br><b>Total time:</b> {trajectory_total_time}",
            align="left",
            xref="paper",
            yref="paper",
            showarrow=False,
            x=0,
            y=-0.1
        )

        if not os.path.exists(".tmp"):
            os.mkdir(".tmp")
        fig.write_html(".tmp/single_track.html", auto_open=True)


if __name__ == '__main__':
    load = PlotlyLoad()
