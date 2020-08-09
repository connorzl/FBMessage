import argparse
import glob
import json
import os
from datetime import datetime
from heapq import nlargest
from tqdm import tqdm

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--path', action='append', type=str, help='Relative path to a messages directory. Repeat this flag to analyze several messages directories together.')
	parser.add_argument('--include_group_chats', dest='group_chats', action='store_true', help='Include group chats in analysis.')
	parser.add_argument('--ignore_group_chats', dest='group_chats', action='store_false', help='Ignore group chats in analysis.')
	parser.set_defaults(path='../../messages/inbox')
	parser.set_defaults(group_chats=True)
	args = parser.parse_args()

	paths = args.path
	for i in range(len(paths)):
		paths[i] = os.path.join(paths[i], 'inbox')

	all_l = []
	for path in paths:
		l = os.listdir(path)
		print("Input path {p} contains {n} files.".format(p=path, n=len(l)))
		all_l += l
	all_l = sorted(all_l, key=str.lower)
	
	lens = []
	nameToCountMap = {}
	for s in tqdm(all_l[1:len(all_l)-1]):
		for path in paths:
			path = os.path.join(path, s)
			try: 
				files = os.listdir(path)
			except:
				continue
			for filename in glob.glob(os.path.join(path, 'message*.json')):
				with open(filename) as f:
					data = json.load(f)

					if not(args.group_chats) and len(data['participants']) > 2:
						continue

					for message in data['messages']:
						sender_name = message['sender_name'].encode("utf-8")
						if sender_name in nameToCountMap:
							nameToCountMap[sender_name] += 1
						else:
							nameToCountMap[sender_name] = 1

	lens = []
	for key in nameToCountMap.keys():
		lens.append([nameToCountMap[key],key])

	x = sorted(lens, key=lambda i: i[0], reverse=True)[:30]

	for l in x:
		print(l)

main()
