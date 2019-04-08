#!/usr/bin/env python3

import os
import re
import codecs
from datetime import datetime


class GMLogParser:
    def __init__(self, logdir):
        if not logdir.endswith("/"):
            logdir += "/"
        files = os.listdir(logdir)
        logs_exist = False
        loglist = []
        for file in files:
            if file.endswith(".log"):
                logs_exist = True
                loglist.append((file, os.path.getmtime(logdir + file)))
        if not logs_exist:
            raise ValueError("Provided directory is not a log folder.")
        self.loglist = sorted(loglist, key=lambda t: t[1])
        self.logdir = logdir
        self.pattern = re.compile(
            '(\d{2}/\d{2}/\d{4}).*(\d{2}:\d{2}:\d{2}): "(.*)<\d*><(STEAM_\d:\d:\d*)><?([a-zA-Z]*)>?"? say "(.*)"')

    def findChat(self, line):
        results = re.search(self.pattern, line)
        if results:
            data = results.groups()
            return {
                "timestamp": int(datetime.strptime(data[0] + " " + data[1], "%m/%d/%Y %H:%M:%S").timestamp()),
                "nick": data[2],
                "steamid": data[3],
                "teamchat": data[4] == "Team",
                "text": data[5]
            }

    def findFileRange(self, startdate, enddate):
        startindex = -1
        endindex = -1

        for i, file in enumerate(self.loglist):
            if startindex == -1 and file[1] > startdate:
                startindex = i
                if not enddate:
                    return startindex, len(self.loglist) - 1
            elif endindex == -1 and enddate and file[1] > enddate:
                return startindex, i

    def getChatLogs(self, startdate, enddate=None, steamids=None):
        daterange = self.findFileRange(startdate, enddate)
        if not daterange:
            return []
        output = []

        for i in range(daterange[0], daterange[1] + 1):
            file = self.loglist[i][0]
            if file.endswith(".log"):
                with codecs.open(self.logdir + file, "r", encoding='utf-8', errors='ignore') as f: # shitty fix for encoding errors with regular open(...)
                    for line in f:
                        result = self.findChat(line)
                        if result and (not steamids or result["steamid"] in steamids):
                            output.append(result)

        return output
