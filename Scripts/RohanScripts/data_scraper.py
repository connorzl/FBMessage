import argparse
import json
from tqdm import tqdm
import string
from wordcloud import WordCloud
import sys
# import matplotlib.pyplot as plt


class MessageCleaner:

    @staticmethod
    def isEmpty(content):
        return content.endswith("sent a photo") or \
               content.endswith("changed the group photo") or \
               content.endswith("waved hello to the group") or \
               content.endswith("sent a video") or \
               content.endswith("sent a location") or \
               content.endswith("sent a sticker") or \
               content.endswith("sent a GIF") or \
               content.endswith("sent a GIF from GIPHY") or \
               content.endswith("sent a photo from Disney Gif") or \
               content.endswith("Tenor GIF Keyboard") or \
               content.endswith("sent a voice message") or \
               content.endswith("sent a location") or \
               content.endswith("sent a live location") or \
               content.endswith("sent an attachment") or \
               "set the nickname" in content or \
               "as a group admin" in content

    @staticmethod
    def clean(message):
        if "content" in message:
            sender = message["sender_name"]
            content = message["content"].encode('ascii', 'ignore').translate(None, string.punctuation)
            return (sender, content)
        else:
            return None


class WordCloudGenerator:
    def __init__(self, chatname):
        self.chatname = chatname
        self.namemap = {}

    def openDataStream(self):
        # return a json data object
        with open(self.chatname, 'r') as f:
           dataStream = json.load(f)
        return dataStream

    def processDataStream(self):
        pass

    def computeWordCloud(self):
        stream = self.openDataStream()

        for data in stream["participants"]:
            self.namemap[data["name"]] = []

        for message in tqdm(stream["messages"]):
            result = MessageCleaner.clean(message)
            if result is None:
                continue
            else:
                sender, content = result
                # people in the chat who arent there anymore
                if sender not in self.namemap:
                    continue
                if MessageCleaner.isEmpty(content):
                    continue
                for word in content.split(" "):
                    self.namemap[sender].append(word)
            
        print("Data processed. Generating wordclouds.")

        for name in tqdm(self.namemap.keys()):
            data = self.namemap[name]
            if len(data) == 0:
                continue
            text = " ".join(data)
            wc = WordCloud().generate(text)
            image = wc.to_image()
            n = name.replace(" ", "")
            image.save(n + "cloud.png")

if __name__=='__main__':
    x = sys.argv[1]
    path = 'messages/inbox/' + x + '/message.json'
    # change path to the path to the message.json blob to analyze
    gen = WordCloudGenerator(path)
    gen.computeWordCloud()
    print("Complete!")
