import os


class ScoreFile():
    """
    Class used to write scores from an algorithm to a csv file.
    """

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.file_path = f"data/scores/{self.file_name}"

    def clear_file(self) -> None:
        """ Clears the csv file from all old data. """

        if os.path.exists(self.file_path):
            # input("WARNING scores file will be deleted.")
            os.remove(self.file_path)

    def prepare_file(self) -> None:
        """ Prepares the csv file for new data, or creates file
            if it does not exist yet. """

        self.clear_file()

        if not (os.path.exists("data/scores") and os.path.isdir("data/scores")):
            os.mkdir("data/scores")

        with open(self.file_path, "w") as file:
            file.write("score\n")

    def write_score(self, score: float) -> None:
        """ Writes given score to the existing csv file. """

        with open(self.file_path, "a") as file:
            file.write(str(score))
            file.write("\n")
