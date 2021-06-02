import pytest
from ..solution import DataProcessor, Journey

VALID_ARRAY = [
    (51.49871493, -0.1601177991, 1326378718),
    (51.49840586, -0.1604068824, 1326378723),
    (51.49820502, -0.1606269428, 1326378728),
    (51.49804155, -0.1605367034, 1326378733),
    (51.49769948, -0.1604581217, 1326378738)
]


class TestDataProcessor:
    def test_unordered_csv(self):
        """
        Check if the processor returns unordered data
        """
        ordered_data = DataProcessor.read_and_preprocess(
            "./tests/csv_unordered.csv")
        assert ordered_data == VALID_ARRAY

    def test_invalid_csv(self):
        """
        Raises value error due to invalid data
        """
        with pytest.raises(ValueError):
            DataProcessor.read_and_preprocess(
                "./tests/csv_invalid.csv")


class TestJourney:
    """
    Tests for the Journey class
    """
    def setup_class(cls):
        cls.journey = Journey(data_points=VALID_ARRAY, valid_speed_limit=200)

    def test_convert_to_km_per_sec(self):
        """
        test convert from kmph to kmps
        """
        expected_value = 0.0556
        actual_value = self.journey.convert_to_km_per_sec(200)
        assert expected_value == round(actual_value, 4)

    def test_calculate_distance(self):
        """
        test calulate haversine distance
        """
        excepted_value = 0.0270
        start = (51.49840586, -0.1604068824)
        end = (51.49820502, -0.1606269428)
        actual_value = self.journey.calculate_distance(start=start, end=end)
        assert excepted_value == round(actual_value, 4)

    def test_calulate_speed(self):
        """
        test calculate speed = distance/time
        """
        excepted_value = 4
        distance = 40
        time = 10
        actual_value = self.journey.calculate_speed(
            distance=distance, time=time)
        assert excepted_value == actual_value

    def test_is_under_limit(self):
        valid_speed = 0.0333
        invalid_speed = 0.8888
        valid_check = self.journey.is_under_limit(valid_speed)
        invalid_check = self.journey.is_under_limit(invalid_speed)

        assert valid_check == True
        assert invalid_check == False

    def test_get_valid_points(self):
        """
        get back only valid data points
        """
        invalid_point = (52.49769948, -0.1604581217, 1326378739)
        invalid_array = VALID_ARRAY + [invalid_point]
        journey_with_invalid_point = Journey(
            data_points=invalid_array, valid_speed_limit=200)

        valid_points = journey_with_invalid_point.get_valid_points()
        assert valid_points == VALID_ARRAY

    def test_journey_intialized_with_empty_array(self):
        """
        Raises value error due to invalid data
        """
        data_points = []
        with pytest.raises(ValueError):
            Journey(data_points=data_points, valid_speed_limit=200)
