import fasttext
import pandas as pd
import numpy as np
import re
import emoji
import tweepy

class FastTextModel:

    def __init__(self, screen_user, api):
        self.screen_user = screen_user
        self.api = api
        #Carregar el model preentrenat de fasttext.
        self.load_model('./data/fastTextModel.model')

    def load_model(self, path):
        self.model = fasttext.load_model(path)

    #Function to clean the text of a tweet.
    def clean_tweet(self, text):
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"/", "", text)
        text = re.sub(r"RT", "", text)
        text = re.sub("\n+", ' ', text)
        text = re.sub("\r+", ' ', text)
        #text = re.sub(r"@.*", "", text) #This do not improve performance.
        #clean_text = re.sub("RT", "", clean_text)
        #clean_text = re.sub("\n", " ", clean_text)
        #clean_text = re.sub("/", "", clean_text)
        #clean_text = re.sub(" +", " ", clean_text)
        #Separate emojis from words.
        """
        sep_emojis_text = ""
        for c in clean_text:
            if c in emoji.UNICODE_EMOJI:
                sep_emojis_text+=' '+c+' '
            else:
                sep_emojis_text+=c
        #This do not improve performance.
        """
        return text

    def getScores(self):
        partiesCountDict = {}
        timeline = self.api.user_timeline(screen_name = self.screen_user, count = 200, include_rts = True,tweet_mode='extended')
        for tweet in timeline:
            parties, scores = self.model.predict(self.clean_tweet(tweet.full_text), k=5)
            #if scores[0] > 0.7:
            #    if parties[0] in partiesCountDict:
            #        partiesCountDict[parties[0]] += 1
            #    else:
            #        partiesCountDict[parties[0]] = 1
            for p,s in zip(parties, scores):
                if s > 0.6:
                    if p in partiesCountDict:
                        partiesCountDict[p] += s
                    else:
                        partiesCountDict[p] = s
        
        sum_scores = np.sum([*partiesCountDict.values()])

        return [(k, v/sum_scores) for k, v in partiesCountDict.items()]