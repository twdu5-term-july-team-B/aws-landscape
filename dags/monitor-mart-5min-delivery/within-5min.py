from datetime import datetime
import sys

# #within-5min.py 2020-07-23 09:30
# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)


# print datetime.strptime(datetimeString, "%y-%m-%d' '%H:%M:%S") - datetime.timedelta(minutes=5)


# curl -i  "http://emr-master.twdu5-term-july-team-b.training:50070/webhdfs/v1/tw/stationMart/data?op=LISTSTATUS"
# {
#   "FileStatuses": {
#     "FileStatus": [
#       {
#         "accessTime": 1595514520058,
#         "blockSize": 134217728,
#         "childrenNum": 0,
#         "fileId": 4990702,
#         "group": "hadoop",
#         "length": 0,
#         "modificationTime": 1595514520059,
#         "owner": "hadoop",
#         "pathSuffix": "_SUCCESS",
#         "permission": "644",
#         "replication": 2,
#         "storagePolicy": 0,
#         "type": "FILE"
#       },
#       {
#         "accessTime": 1595514520039,
#         "blockSize": 134217728,
#         "childrenNum": 0,
#         "fileId": 4990701,
#         "group": "hadoop",
#         "length": 129674,
#         "modificationTime": 1595514520049,
#         "owner": "hadoop",
#         "pathSuffix": "part-00000-06eb7428-ce1e-4e93-bc81-552023c806ca-c000.csv",
#         "permission": "644",
#         "replication": 2,
#         "storagePolicy": 0,
#         "type": "FILE"
#       }
#     ]
#   }
# }
