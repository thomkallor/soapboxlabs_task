import csv
from haversine import haversine

from typing import final, List, Tuple

DataPoint = Tuple[float, float, int]
Location = Tuple[float, float]


class DataProcessor:

    @staticmethod
    def read_and_preprocess(path: str) -> List[DataPoint]:
        """
        Read csv file raises error if the data is invalid
        The Data should be in (latitude, longitude, timestamp) format
        Sorts the 2D array by timestamp
        """
        data_points = []
        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            for row in reader:
                data_points.append(
                    (float(row[0]),
                     float(row[1]),
                     int(row[2])
                     )
                )
        data_points.sort(key=lambda row: row[2])
        return data_points

    @staticmethod
    def write(data: List[DataPoint], path: str) -> None:
        """
        Write the data to the path mentioned
        """
        with open(path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)


class Journey:
    """
    Journey represents a list of valid DataPoints
    Raise error if length is lesser than 2
    """
    _data_points: List[DataPoint]
    _valid_speed_limit: float

    def __init__(self,
                 data_points: List[DataPoint],
                 valid_speed_limit: int) -> None:

        if(len(data_points) < 2):
            raise ValueError("Not a valid journey")

        self._data_points = data_points
        self._valid_speed_limit = self.convert_to_km_per_sec(valid_speed_limit)

    @final
    def convert_to_km_per_sec(self, speed) -> float:
        """
        Convert kmph to km/sec
        """
        kmps = speed / 3600
        return kmps

    def calculate_distance(self, start: Location, end: Location) -> float:
        """
        Calculate distance between 2 co-ordinates in km
        Uses haversine formula
        """
        return haversine(start, end)

    def calculate_speed(self, distance: float, time: int) -> float:
        """
        Calculate Speed
        """
        return distance / time

    def is_under_limit(self, speed) -> bool:
        """
        Returns True if the speed is under limit
        """
        is_valid = speed <= self._valid_speed_limit
        return is_valid

    def get_valid_points(self) -> List[DataPoint]:
        """
        Check if the speed is under the valid limit
        Assumes that the first point encountered is always right
        Assumes that there are no duplicate timestamps
        Returns list of valid data points
        """
        valid_data_points = [self._data_points[0]]
        num_rows = len(self._data_points)

        # valid_head contains the last valid point
        # current_head contains the current index to check
        valid_head = 0
        current_head = 1

        while (current_head < num_rows):

            start_data_point: DataPoint = self._data_points[valid_head]
            end_data_point: DataPoint = self._data_points[current_head]

            time_travelled: int = end_data_point[2] - start_data_point[2]
            start_location: Location = (
                start_data_point[0], start_data_point[1])
            end_location: Location = (end_data_point[0], end_data_point[1])

            distance_travelled = self.calculate_distance(
                start_location, end_location)
            speed = self.calculate_speed(
                distance_travelled, time_travelled)

            if self.is_under_limit(speed):
                valid_data_points.append(self._data_points[current_head])
                valid_head = current_head

            current_head += 1

        return valid_data_points


if __name__ == "__main__":
    dataset_path = "data_points.csv"
    # speed limit in kmph
    speed_limit = 200
    initial_data = DataProcessor.read_and_preprocess(dataset_path)
    journey = Journey(data_points=initial_data, valid_speed_limit=speed_limit)
    valid_points = journey.get_valid_points()
    DataProcessor.write(valid_points, "valid_points.csv")
