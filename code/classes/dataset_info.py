class DatasetInfo:
    """ Private class, do not use. """

    def __init__(self, dataset: str):
        """ Creates a DatasetInfo object. """
        self.__dataset = dataset

        self.number_of_connections: int = self.__get_number_of_connections()
        self.number_of_stations: int = self.__get_number_of_stations()
        self.max_trajectories: int = self.__get_max_trajectories()
        self.max_trajectory_length: int = self.__get_max_trajectory_length()

    def __get_number_of_connections(self) -> int:
        """ Private method to assign number of connections. """
        if self.__dataset == "holland":
            return 28
        elif self.__dataset == "nationaal":
            return 89
        else:
            raise TypeError

    def __get_number_of_stations(self) -> int:
        """ Private method to assign number of stations. """
        if self.__dataset == "holland":
            return 22
        elif self.__dataset == "nationaal":
            return 61
        else:
            raise TypeError

    def __get_max_trajectories(self) -> int:
        """ Private method to assign number max of trajectories. """
        if self.__dataset == "holland":
            return 7
        elif self.__dataset == "nationaal":
            return 20
        else:
            raise TypeError

    def __get_max_trajectory_length(self) -> int:
        """ Private method to assign max length of trajectory. """
        if self.__dataset == "holland":
            return 120
        elif self.__dataset == "nationaal":
            return 180
        else:
            raise TypeError
