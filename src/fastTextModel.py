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
        return text

    def getScores(self):
        partiesCountDict = {}
        timeline = self.api.user_timeline(screen_name = self.screen_user, count = 200, include_rts = True,tweet_mode='extended')
        #Si l'usuari te menys de 100 tweets (50% dels que analitzem) no efectuem una resposta.
        if len(timeline) <= 100: return []
        for tweet in timeline:
            text = tweet.retweeted_status.full_text if tweet.full_text.startswith("RT @") else tweet.full_text
            parties, scores = self.model.predict(self.clean_tweet(text), k=5)
            for p,s in zip(parties, scores):
                if s > 0.6: #Si el tweet te una probabilitat de mes del 60% de ser del partit actual.
                    if p in partiesCountDict:
                        partiesCountDict[p] += s
                    else:
                        partiesCountDict[p] = s
        
        sum_scores = np.sum([*partiesCountDict.values()])

        return [(k, v/sum_scores) for k, v in partiesCountDict.items()]