from .dataset_info import DatasetInfo


class DataInfo:
    """
    Class to store basic properties about the data.
    Can be accessed at any time.
    Class is static and does not have an initializer.

    Usage:
    DataInfo.dataset.property
    dataset in {"holland", "nationaal"}
    property in {"number_of_connections",
                 "number_of_stations",
                 "max_trajectories",
                 "max_trajectory_length"}
    """

    holland: DatasetInfo = DatasetInfo(dataset="holland")
    nationaal: DatasetInfo = DatasetInfo(dataset="nationaal")
