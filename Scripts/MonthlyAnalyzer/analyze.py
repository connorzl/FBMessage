import time
import datetime
import json
import calendar
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

file_name = "../../messageFiles/sele/message.json"

with open(file_name, "r") as read_file:
    data = json.load(read_file)

count_dictionary = {}
oldestYear = 2020
for message in data["messages"]:
    message_time = datetime.datetime.fromtimestamp(int(message["timestamp_ms"])/1000.0)
    year = message_time.year
    month = message_time.month
    if year < oldestYear: oldestYear = year
    if year not in count_dictionary:
        count_dictionary[year] = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
    count_dictionary[year][month] += 1


heights = []
names = []
for x in xrange(len(count_dictionary)):
    startingYear = x + oldestYear
    for month in xrange(1,13):
        xtick = str(month) +"-"+ str(startingYear)
        names.append(xtick)
        heights.append(count_dictionary[startingYear][month])

y_pos = np.arange(len(heights))


plt.bar(y_pos,heights,align='center')
plt.title(data["title"])
plt.xticks(y_pos,names,rotation=70)
plt.ylabel("Messages/Month")
plt.xlabel("Month-Year")
plt.show()
