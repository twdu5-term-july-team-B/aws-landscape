import unittest
from monitor_application_streaming_queue.monitor_application_streaming_queue import MonitorApplicationStreamingQueue
import json


class MonitorConsumersRunningTest(unittest.TestCase):
    def test_parse(self):
        monitorApplicationStreamingQueue = MonitorApplicationStreamingQueue()
        with open('testcase.json') as json_file:
            test_dict = json.load(json_file)

        self.assertEqual(['StationDataSFSaverApp'], monitorApplicationStreamingQueue.parse(test_dict))

if __name__ == '__main__':
    unittest.main()
