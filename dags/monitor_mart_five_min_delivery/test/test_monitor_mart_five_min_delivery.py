import unittest
from dags.monitor_mart_five_min_delivery.monitor_mart_five_min_delivery import calculate_metric_data_value, get_last_modification_epoch, is_within_five_minute_delivery
import json
import mock
from datetime import datetime


class MyTestCase(unittest.TestCase):
    @mock.patch('dags.monitor_mart_five_min_delivery.monitor_mart_five_min_delivery.datetime')
    def test_fetch_modification_times(self, mock_dt):
        with open('testcase.txt') as json_file:
            test_dict = json.load(json_file)
        mock_dt.utcnow = mock.Mock(return_value=datetime(2020, 07, 23, 14, 28, 40, 59))

        self.assertEqual(1595514520059/1000, get_last_modification_epoch(test_dict))

    def test_is_within_five_minute_delivery(self):
        self.assertEqual(False, is_within_five_minute_delivery(1595514520059))




    def test_calculate_metric_data_value_for_file_that_has_been_written_in_the_last_five_min(self):
      self.assertEqual(calculate_metric_data_value(True), 1.0)

    def test_calculate_metric_data_value_for_file_that_has_not_been_written_in_the_last_five_min(self):
      self.assertEqual(calculate_metric_data_value(False), 0.0)

if __name__ == '__main__':
    unittest.main()
