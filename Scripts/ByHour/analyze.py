import time
import datetime
import json
import calendar
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from tqdm import tqdm
from operator import add
file_name = "../../messageFiles/Vay/message.json"

with open(file_name, "r") as read_file:
    data = json.load(read_file)


count_dictionary = {}
for p in data["participants"]:
    count_dictionary[p["name"]] = [0 for i in xrange(24)]

# first index is used for total message count, others are for the hours.
for message in tqdm(data["messages"]):
    message_time = datetime.datetime.fromtimestamp(int(message["timestamp_ms"])/1000.0)
    hour = message_time.hour
    name = message["sender_name"]
    if name not in count_dictionary: # takes care of case when people not in chat anymore
        continue
    count_dictionary[name][hour] +=1

f, axarr = plt.subplots(len(count_dictionary.keys()), sharex=True,sharey=True)
f.suptitle("Time Analysis of " + data["title"])
print len(axarr)
index= 0
labels = [str(i) for i in xrange(24)]
print labels
for name in count_dictionary:
    y_pos = np.arange(len(count_dictionary[name]))
    axarr[index].bar(y_pos,count_dictionary[name])
    axarr[index].set_xticks(y_pos,labels)
    axarr[index].set_title(name)

    index+=1

plt.show()
    
    