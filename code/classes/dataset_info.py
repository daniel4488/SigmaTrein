class DatasetInfo:
    """ Private class, do not use. """

    def __init__(self, dataset: str):

        self.__dataset = dataset

        self.total_connections: int = self.__get_total_connections()
        self.total_stations: int = self.__get_total_stations()
        self.max_trajectories: int = self.__get_max_trajectories()
        self.max_time: int = self.__get_max_time()

    def __get_total_connections(self) -> int:
        """ Private method to assign number of connections. """

        if self.__dataset == "holland":
            return 28
        elif self.__dataset == "nationaal":
            return 89
        else:
            raise TypeError

    def __get_total_stations(self) -> int:
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

    def __get_max_time(self) -> int:
        """ Private method to assign max length of trajectory. """

        if self.__dataset == "holland":
            return 120
        elif self.__dataset == "nationaal":
            return 180
        else:
            raise TypeError
