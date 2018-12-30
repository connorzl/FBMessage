import os
import json
from datetime import datetime
from heapq import nlargest

def main():
	path = "../../messages/inbox"
	l = os.listdir(path) # dir is your directory path
	number_files = len(l)
	print(number_files)

	l = sorted(l, key=str.lower)
	# testL = l[1:10]

	lens = []

	for s in l[1:len(l)-1]:
		files = os.listdir(path + "/" + s)
		with open(path + "/" + s + '/message.json') as f:
			data = json.load(f)

			if len(data['participants']) > 2:
				continue

			names = []
			for p in data['participants']:
				names.append(p['name'].encode("utf-8"))
			# print(names)

			messages = data['messages']

			lens.append([len(messages), s])
			# print(len(messages))
			# for m in messages:
			# 	time = m["timestamp_ms"]/1000
			# 	print(datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))


	x = sorted(lens, key=lambda i: i[0], reverse=True)[:30]

	for l in x:
		print(l)
	print(x)

main()