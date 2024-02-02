import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os


class DistCompare:

    def __init__(self) -> None:
        self.directory: str = "code/scripts/dist_compare/1/"
        self.csv_files: list[str] = glob.glob(self.directory + "*.csv")
        # self.colors: list[str] = ["skyblue", "red"]
        self.df: pd.DataFrame = self.load_csv_files()
        print(self.df.head())
        self.visualize()

    def load_csv_files(self) -> pd.DataFrame:
        # list for storing separate dataframes
        dfs = []

        # load all csv files
        for file in self.csv_files:
            df = pd.read_csv(file)
            df.rename(
                columns=dict(zip(df.columns, [os.path.splitext(file.split("/")[-1])[0].capitalize()])),
                inplace=True
            )
            dfs.append(df)

        # merge all dataframes into one dataframe
        return pd.concat(dfs, axis=1, ignore_index=False)

    def visualize(self) -> None:
        sns.set(style="darkgrid")
        # for algorithm in self.df.columns.tolist():
        #     color = self.colors.pop()
        #     ax = sns.histplot(data=self.df, x=algorithm, color=color, label=algorithm, kde=True)
        ax = sns.histplot(data=self.df, kde=True, palette="deep", legend=True)
        ax.set(xlabel="Score", ylabel="Frequency")
        # plt.legend(labels=self.df.columns.tolist())
        # plt.show()
        plt.savefig(f"{self.directory}dist_compare.svg", format="svg")


if __name__ == "__main__":
    DistCompare()
