"""

Brandon Dunbar
PowerBI Computer Stat Monitoring

"""

# Imports
import urllib.request as urllib
import psutil
import os, time, json
from datetime import datetime

# PowerBI LiveStream URLs
REST_API_URL = "https://api.powerbi.com/beta/514efd40-8efe-4f15-819f-34e56acf1562/datasets/0f12502f-72f1-489e-bb74-72b8e806b416/rows?key=6MVPRRyL1BHVE08EkrygfOJflP5PX%2Fy0EmlpV%2BQP3ZhcmURJtri27oIDUrtob7PzCjF7qvZJCQpGdBmJe%2B6jdA%3D%3D"

# Set initial values for bytes sent/received
bytes_sent = float(psutil.net_io_counters()[0])
bytes_received = float(psutil.net_io_counters()[1])

try:
    # Infinite loop
    while True:

        # Get the difference in bytes sent/received since last check:
        _new_bytes_sent = float(psutil.net_io_counters()[0])
        _new_bytes_received = float(psutil.net_io_counters()[1])
    
        bytes_sent_diff = _new_bytes_sent - bytes_sent
        bytes_received_diff = _new_bytes_received - bytes_received

        # Data grab
        stats = [{
                "time_stamp": datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z"),
                "disk_usage": float(psutil.disk_usage("c:")[-1]),
                "cpu_usage": float(psutil.cpu_percent(interval=0.1)),
                "virtual_memory": float(psutil.virtual_memory()[2]),
                "battery": float(psutil.sensors_battery()[0]),
                "bytes_sent": bytes_sent_diff,
                "bytes_received": bytes_received_diff
                }]

        bytes_sent = _new_bytes_sent
        bytes_received = _new_bytes_received
    
        # Convert dictionary to JSON then Bytes - preparing to send
        data = bytes(json.dumps(stats), "utf-8")
    
        # PowerBI push
        req = urllib.Request(REST_API_URL, data=data)
        response = urllib.urlopen(req)

        # Sleep
        time.sleep(5)

finally:

    print("Program ended.")
