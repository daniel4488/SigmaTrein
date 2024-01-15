import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


def read_score_file():
    data = pd.read_csv("data/scores/random.csv")
    data.head()
    return data


def visualize_baseline() -> None:
    # get scores from csv file
    scores = read_score_file()

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


def visualize_iterations_to_score() -> None:
    # get scores from csv file
    scores = read_score_file()

    # create graph
    fig = px.line(scores, x = range(len(scores)), y = 'score', labels = {
                  'x': 'Iterations',
                  'score': 'Score'},
                  title = 'Scores of 100 iterations from a random algorithm')
    fig.show()


if __name__ == "__main__":
    visualize_baseline()
    visualize_iterations_to_score()
