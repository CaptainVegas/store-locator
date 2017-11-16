import unittest
from find_store import convert_km_to_miles
from find_store import find_distance_to_store
from find_store import find_closest_store
from find_store import get_location_data
from find_store import load_store_location_data

class FindStoreTestCase(unittest.TestCase):
    """Tests for `find_store.py`."""

    def test_load_store_location_data(self):
        """Test if we can successfully load the store location data"""
        self.assertTrue(load_store_location_data() is not None)

    def test_get_location_data(self):
        """Test if Google thinks Beverly Hills exists"""
        self.assertTrue(get_location_data('90210') is not None)

    def test_find_closest_store(self):
        """Test if we can successfuly find the closet Latitude and Longitude in our test store location data"""
        test_store_location_data = [{'Latitude': 39.7612992, 'Longitude': -86.1519681}, 
                                    {'Latitude': 39.7622412, 'Longitude': -86.1584362}, 
                                    {'Latitude': 39.7622292, 'Longitude': -86.1578917}]

        test_query_coordinates = {'Latitude': 37.9696551, 'Longitude': -122.5276637}
        closet_store = find_closest_store(test_store_location_data, test_query_coordinates)
        self.assertTrue(closet_store['Latitude'] == 39.7622412 and closet_store['Longitude'] == -86.1584362)

    def test_find_distance_to_store(self):
        """Test if the distance between the Golden Gate Bridge and the Empire State building is what we expect"""
        self.assertTrue(find_distance_to_store(37.8078124, -122.47516439999998, 40.74871, -73.985656) == 4134.596435348435)

    def test_convert_km_to_miles(self):
        """Test if converting 20 kilometers to miles gives the result we expect"""
        self.assertTrue(convert_km_to_miles(20) == 12.42742)

if __name__ == '__main__':
    unittest.main()