import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


def visualize_baseline() -> None:
    scores = pd.read_csv("data/scores/random.csv")
    scores.head()

    line_settings = {
        "linewidth": "2"
    }

    fig = sns.histplot(scores["score"], kde=True, line_kws=line_settings)

    plot_settings = {
        "title": f"Random Algorithm with {len(scores):,} simulations",
        "xlabel": "Score"
    }

    fig.set(**plot_settings)
    plt.show()

    # Export graph
    plt.savefig("code/visualisation/baseline.svg", format="svg")


def visualize_iterations_to_score() -> None:
    scores = pd.read_csv("data/scores/random.csv")
    scores.head()

    fig = px.line(scores, x = range(len(scores)), y = 'score', labels = {
                  'x': 'Iterations',
                  'score': 'Score'},
                  title = 'Scores of 100 iterations from a random algorithm')
    fig.show()


if __name__ == "__main__":
    visualize_baseline()
    visualize_iterations_to_score()
