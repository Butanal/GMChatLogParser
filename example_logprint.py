import gmlogparser
from datetime import datetime

def format_date(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%H:%M:%S")

logparser = gmlogparser.GMLogParser("/path/to/log/folder")

logs = logparser.getChatLogs(startdate=1052479002, steamids=("STEAM_0:0:0"))
for log in logs:
    print("[{}] {} : \"{}\"".format(format_date(log["timestamp"]), log["nick"], log["text"]))
