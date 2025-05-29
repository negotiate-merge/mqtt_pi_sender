from datetime import datetime, timedelta
import json
import random
import time

# Get the last hour
def get_last_hour(dt=None, interval=60):
  if dt is None:
    dt = datetime.now()
    last_hour = dt - timedelta(minutes=dt.minute % interval, seconds=dt.second, microseconds=dt.microsecond)
    if last_hour.hour % 2 > 0: last_hour -= timedelta(hours=1)
  return last_hour


# Get last data sent time
def get_last_uploaded():
  with open("upload_times.txt", "r") as f:
    last_line = f.readlines()[-1].strip()
  return datetime.strptime(last_line, "%Y-%m-%d %H:%M:%S")


def generateFloat():
  return round(random.uniform(0, 3.4), 3)

def get_messages():
  last_hour = get_last_hour()
  last_upload = get_last_uploaded()
  time_diff = abs(last_hour - last_upload)

  dev_ids = [
    '863663062798815',
    '863663062798816',
    'aabbccddeeff0003',
    'aabbccddeeff0004',
    'aabbccddeeff0005',
  ]

  times = [
    last_upload + timedelta(minutes=15),
    last_upload + timedelta(minutes=30),
    last_upload + timedelta(minutes=45),
    last_upload + timedelta(minutes=60),
    last_upload + timedelta(minutes=75),
    last_upload + timedelta(minutes=90),
    last_upload + timedelta(minutes=105),
    last_upload + timedelta(minutes=120),
  ]

  msgs = []

  # print(time_diff)
  if time_diff >= timedelta(hours=2):  # Change this back to 2 when ready
    # We will generate the data
    for d in dev_ids:
      msg = {
        "IMEI": d,
        "IMSI": "460083513507309",
        "Model": "PS-NB",
        "idc_input": 0.000,
        "vdc_input": 9.934,
        "battery": 3.587,
        "signal": 25,
        "time": times[7].strftime("%Y-%m-%d %H:%M:%S"),
        "1":[generateFloat(),generateFloat(), times[0].strftime("%Y-%m-%d %H:%M:%S")],
        "2":[generateFloat(),generateFloat(), times[1].strftime("%Y-%m-%d %H:%M:%S")],
        "3":[generateFloat(),generateFloat(), times[2].strftime("%Y-%m-%d %H:%M:%S")],
        "4":[generateFloat(),generateFloat(), times[3].strftime("%Y-%m-%d %H:%M:%S")],
        "5":[generateFloat(),generateFloat(), times[4].strftime("%Y-%m-%d %H:%M:%S")],
        "6":[generateFloat(),generateFloat(), times[5].strftime("%Y-%m-%d %H:%M:%S")],
        "7":[generateFloat(),generateFloat(), times[6].strftime("%Y-%m-%d %H:%M:%S")],
        "8":[generateFloat(),generateFloat(), times[7].strftime("%Y-%m-%d %H:%M:%S")],
      }
      # print(json.dumps(msg, indent=2))
      msgs.append(msg)

    # Uncomment to run properly
    with open("upload_times.txt", "a") as f:
      f.write(last_hour.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    
  return msgs

