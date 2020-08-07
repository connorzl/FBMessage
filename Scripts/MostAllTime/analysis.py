import os
import json
from datetime import datetime
from heapq import nlargest
from tqdm import tqdm
import glob

def main():
	path = "../../messages/inbox"
        # path = "../../../facebookdata/messages/inbox"
	l = os.listdir(path) # dir is your directory path
	number_files = len(l)
	print(number_files)

	l = sorted(l, key=str.lower)
	# testL = l[1:10]

	lens = []

	nameToCountMap = {}

	for s in tqdm(l[1:len(l)-1]):
		files = os.listdir(path + "/" + s)
		for filename in glob.glob(path + "/" + s + '/message*.json'):
			with open(filename) as f:
				data = json.load(f)

				if len(data['participants']) > 2:
					continue

				names = []
				for p in data['participants']:
					names.append(p['name'].encode("utf-8"))

				messages = data['messages']
				for name in names:
					if name in nameToCountMap:
						nameToCountMap[name] = nameToCountMap[name] + len(messages)
					else:
						nameToCountMap[name] = len(messages)



				# lens.append([len(messages), names])
				# print(len(messages))
				# for m in messages:
				# 	time = m["timestamp_ms"]/1000
				# 	print(datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
	lens = []
	for key in nameToCountMap.keys():
		lens.append([nameToCountMap[key],key])

	# print nameToCountMap


	x = sorted(lens, key=lambda i: i[0], reverse=True)[:30]

	for l in x:
		print(l)

main()
