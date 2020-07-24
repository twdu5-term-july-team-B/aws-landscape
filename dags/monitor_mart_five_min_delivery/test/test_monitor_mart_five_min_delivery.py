import unittest
from monitor_mart_five_min_delivery.monitor_mart_five_min_delivery import calculate_metric_data_value, time_difference_since_last_modified
import json

class MyTestCase(unittest.TestCase):
    def test_fetch_modification_times(self):
        with open('testcase.txt') as json_file:
            test_dict = json.load(json_file)

        self.assertEqual(['1595514520059', '1595514520049'], time_difference_since_last_modified(test_dict))

    def test_calculate_metric_data_value_for_file_that_has_been_written_in_the_last_five_min(self):
      self.assertEqual(calculate_metric_data_value(True), 1.0)

    def test_calculate_metric_data_value_for_file_that_has_not_been_written_in_the_last_five_min(self):
      self.assertEqual(calculate_metric_data_value(False), 0.0)

if __name__ == '__main__':
    unittest.main()
