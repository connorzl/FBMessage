import time
import datetime
import json
import calendar
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from operator import add
file_name = "../../messageFiles/flaker/message.json"

with open(file_name, "r") as read_file:
    data = json.load(read_file)

count_dictionary = {}
oldestYear = 2020
for message in tqdm(data["messages"]):
    message_time = datetime.datetime.fromtimestamp(int(message["timestamp_ms"])/1000.0)
    year = message_time.year
    month = message_time.month
    name = message["sender_name"]
    if year < oldestYear: oldestYear = year
    if year not in count_dictionary:
        count_dictionary[year] = {}
        for month in xrange(1,13):
            count_dictionary[year][month] = {}
            for person in data["participants"]:
                count_dictionary[year][month][person["name"]] = 0
    if name not in count_dictionary[year][month]:
        continue
    count_dictionary[year][month][name] += 1

heights = []
sheights = []
for person in data["participants"]:
    heights.append([])


names = []
for x in xrange(len(count_dictionary)):
    startingYear = x + oldestYear
    for month in xrange(1,13):
        xtick = str(month) +"-"+ str(startingYear)
        names.append(xtick)
        if startingYear not in count_dictionary:
            for h in heights:
                h.append(0)
        else:
            for i in xrange(len(heights)):
                heights[i].append(count_dictionary[startingYear][month][data["participants"][i]["name"]])

sumheights = [heights[0]]
for i in xrange(1,len(heights)):
    sumheights.append(list(map(add,sumheights[i-1],heights[i])))


colors = ['b','g','r','c','m','y','k','w','.75']
y_pos = np.arange(len(heights[0]))
p = [plt.bar(y_pos,heights[0],align='center',color=colors[0])]
for i in xrange(1,len(heights)):
    p.append(plt.bar(y_pos,heights[i],bottom=sumheights[i-1],align='center',color=colors[i]))
plt.title(data["title"])
plt.xticks(y_pos,names,rotation=70)
plt.ylabel("Messages/Month")
plt.xlabel("Month-Year")
t1 = []
t2  = []
for i in xrange(len(heights)): #create legend
    t1.append(p[i][0])
    t2.append(data["participants"][i]["name"])

plt.legend(tuple(t1), tuple(t2),loc='best')

plt.show()

# print heights
