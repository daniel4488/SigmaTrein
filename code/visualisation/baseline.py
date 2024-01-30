import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

import os


def read_score_file(data: str):
    # data = pd.read_csv("data/scores/random.csv")
    data = pd.read_csv(data)
    data.head()
    return data


def visualize_baseline(data: str) -> None:
    """ Plots the scores from the given data against their occurence. """

    # get scores from csv file
    scores = read_score_file(data)

    # set line settings
    line_settings = {
        "linewidth": "2"
    }

    # create histogram
    fig = sns.histplot(scores["score"], kde=True, line_kws=line_settings)

    plot_settings = {
        "title": f"Random Algorithm with {len(scores):,} simulations",
        "xlabel": "Score"
    }

    fig.set(**plot_settings)
    plt.show()

    # export graph
    plt.savefig("code/visualisation/baseline.svg", format="svg")


def visualize_iterations_to_score(data: str) -> None:
    """ Plots scores from a csv file against the iteration. """

    # get scores from csv file
    scores = read_score_file(data)
    algorithm = os.path.splitext(data)[0].split("/")[-1].replace("_", " ")

    # create graph
    fig = px.line(scores, x=range(len(scores)), y="score", labels={
        "x": "Iterations",
        "score": "Score"
        },
        title=f"Scores of {len(scores)} iterations from a {algorithm} algorithm")
    # fig.update_yaxes(range=[0, 10000])
    # plt.show()
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    fig.write_html(".tmp/iter_to_score.html", auto_open=False)


if __name__ == "__main__":
    data = "data/scores"
    visualize_baseline(data)
    visualize_iterations_to_score(data)
