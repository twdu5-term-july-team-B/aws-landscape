import unittest
from monitor_mart_five_min_delivery.monitor_mart_five_min_delivery import calculate_metric_data_value, get_last_modification_epoch, is_within_five_minute_delivery
import json
import mock
from datetime import datetime


class MonitorMartFiveMinDeliveryTest(unittest.TestCase):
    def test_fetch_modification_times(self):
        with open('testcase.txt') as json_file:
            test_dict = json.load(json_file)

        self.assertEqual(1595514520049, get_last_modification_epoch(test_dict))

    @mock.patch('monitor_mart_five_min_delivery.monitor_mart_five_min_delivery.datetime')
    def test_is_within_five_minute_delivery(self, mock_dt):
        mock_dt.utcnow = mock.Mock(return_value=datetime.fromtimestamp(1595514520059/1000))
        self.assertTrue(is_within_five_minute_delivery(1595514520059))

    def test_is_within_five_minute_delivery(self):
        self.assertFalse(is_within_five_minute_delivery(1595514520059))


    def test_calculate_metric_data_value_for_file_that_has_been_written_in_the_last_five_min(self):
        self.assertEqual(calculate_metric_data_value(True), 1.0)

    def test_calculate_metric_data_value_for_file_that_has_not_been_written_in_the_last_five_min(self):
        self.assertEqual(calculate_metric_data_value(False), 0.0)

if __name__ == '__main__':
    unittest.main()
