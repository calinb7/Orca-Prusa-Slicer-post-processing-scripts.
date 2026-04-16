#!/usr/bin/env python

"""
Adapted by calinb to extract print time.
Credit to @author: Maciej Wanat
(https://github.com/MaciejWanat/ender-v3-prusa-preview-data)
"""

import re
import sys

def parseTimeString(timeComponents):
    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    for value, unit in timeComponents:
        value = int(value)
        if unit == 'd':
            days += value
        elif unit == 'h':
            hours += value
        elif unit == 'm':
            minutes += value
        elif unit == 's':
            seconds += value

    totalSeconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
    return totalSeconds

header = ""

bottomLinesAnalyzedAmount = 800

sourceFile = sys.argv[1]
print(sourceFile)
with open(sourceFile, 'r+') as file:
    content = file.readlines()
    lines = ''.join(content[-bottomLinesAnalyzedAmount:])

    # expected example: -> ; estimated printing time (normal mode) = 9h 56m 19s
    timeEstimatedPrusaData = re.findall(r'; estimated printing time \(normal mode\) = .*', lines)[0]

    timeComponents = re.findall(r'(\d+)([dhms])', timeEstimatedPrusaData)
    secondsTotal = parseTimeString(timeComponents)

    header += f';TIME:{secondsTotal}\n'

    file.seek(0, 0)
    file.write(header)
    file.writelines(content)
