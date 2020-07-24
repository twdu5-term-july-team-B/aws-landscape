import unittest
from monitor_mart_five_min_delivery.monitor_mart_five_min_delivery import fetch_modification_times_from_response
from monitor_mart_five_min_delivery.monitor_mart_five_min_delivery import calculateMetricDataValue


class MyTestCase(unittest.TestCase):
    def test_something(self):
        test_dict = {
              "FileStatuses": {
                "FileStatus": [
                  {
                    "accessTime": 1595514520058,
                    "blockSize": 134217728,
                    "childrenNum": 0,
                    "fileId": 4990702,
                    "group": "hadoop",
                    "length": 0,
                    "modificationTime": 1595514520059,
                    "owner": "hadoop",
                    "pathSuffix": "_SUCCESS",
                    "permission": "644",
                    "replication": 2,
                    "storagePolicy": 0,
                    "type": "FILE"
                  },
                  {
                    "accessTime": 1595514520039,
                    "blockSize": 134217728,
                    "childrenNum": 0,
                    "fileId": 4990701,
                    "group": "hadoop",
                    "length": 129674,
                    "modificationTime": 1595514520049,
                    "owner": "hadoop",
                    "pathSuffix": "part-00000-06eb7428-ce1e-4e93-bc81-552023c806ca-c000.csv",
                    "permission": "644",
                    "replication": 2,
                    "storagePolicy": 0,
                    "type": "FILE"
                  }
                ]
              }
        }
        self.assertEqual(fetch_modification_times_from_response(test_dict), ['1595514520059', '1595514520049'])

    def test_calculateMetricDataValueForFileThatHasBeenWrittenInTheLastFiveMin(self):
      self.assertEqual(calculateMetricDataValue(True), 1.0)

    def test_calculateMetricDataValueForFileThatHasNotBeenWrittenInTheLastFiveMin(self):
      self.assertEqual(calculateMetricDataValue(False), 0.0)

if __name__ == '__main__':
    unittest.main()
