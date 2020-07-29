import unittest
from monitor_consumers_running.monitor_consumers_running import MonitorConsumersRunning
import json


class MonitorConsumersRunningTest(unittest.TestCase):
    def test_parse(self):
        monitorConsumersRunning = MonitorConsumersRunning()
        with open('testcase.json') as json_file:
            test_dict = json.load(json_file)

        self.assertEqual(['StationDataSFSaverApp'], monitorConsumersRunning.parse(test_dict))

if __name__ == '__main__':
    unittest.main()
