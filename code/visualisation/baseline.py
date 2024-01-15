import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def visualize_baseline() -> None:
    scores = pd.read_csv("data/scores/random.csv")
    print(scores.head())

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


if __name__ == "__main__":
    visualize_baseline()
