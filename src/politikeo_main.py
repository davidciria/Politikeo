import tweepy
import json
import numpy as np
from config import create_api
import time 
from fastTextModel import FastTextModel
from decisionModel import DecisionModel
import nltk
import os
import re
#Download nltk stopwords.
if 'stopwords' not in os.listdir( nltk.data.find("corpora") ):
  nltk.download('stopwords')

class PolitikeoStreamer(tweepy.StreamListener):
    def __init__(self, api):
      self.api = api
      self.me = api.me()

    def predict_user(self, screen_user):
      #L'ordre dels partits en el model de decisio es Vox, PP, Ciudadanos, PSOE, UP.
      parties_order = ["vox", "pp", "cs", "psoe", "up"] #Array per saber l'ordre.
      userDecisionModel = DecisionModel(screen_user, self.api)
      emojisScores = list(userDecisionModel.emojisScores())
      keywordsScores = list(userDecisionModel.keywordsScores())
      decisionModelScores = np.add(emojisScores, keywordsScores)
      decisionModelScores = list(zip(decisionModelScores, parties_order)) #Zip amb el nom dels partits.
      decisionModelScores.sort(key=lambda tup: tup[0], reverse=True) #Ordenem descendentment.
      print(decisionModelScores)
      #Si tenim un score significant. El primer es el doble que el segon.
      if (decisionModelScores[0][0] >= 0.25) and (2*decisionModelScores[1][0] <= decisionModelScores[0][0]):
        #Retornem el partit politic.
        return decisionModelScores[0][1]
      else:
        #Apliquem fasttext.
        fastTextModel = FastTextModel(screen_user, self.api)
        fastTextModelScores = fastTextModel.getScores()
        fastTextModelScores.sort(key=lambda tup: tup[1], reverse=True)
        print(fastTextModelScores)
        #Si el score de fasttext es major del 40%, retornem la prediccio.
        if(fastTextModelScores[0][1] >= 0.4):
          return re.sub(r"__label__", "", fastTextModelScores[0][0])
        else:
          #No hem estat capaços de preedir el partit.
          return None

    def getPhotoDir(self, partyLabel):
      parties_photos = {"vox": "./data/media/vox.png", "pp": "./data/media/pp.png", "cs": "./data/media/cs.png", "psoe": "./data/media/psoe.png", "up": "./data/media/up.png"}
      return parties_photos[partyLabel]

    def on_status(self, tweet):
      # Informacio del tweet que ens ha mencionat.
      tweet_id = tweet.id
      tweet_screen_user = tweet.user.screen_name
      if tweet.user.screen_name != self.me.screen_name:
        users_called = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-.]))@([A-Za-z]+[A-Za-z0-9-]+)', tweet.text)
        users_called_processed = [u for u in list(set(users_called)) if u!=tweet.user.screen_name and u!=self.me.screen_name]  #Eliminem duplicats i obtenim usuaris diferents.
        # Processament del partit politic del usuari.
        predicted_party_label = self.predict_user(tweet_screen_user)

        #No hem pogunt determinar la ideologia de l'usuari.
        if predicted_party_label is None:
          self.api.update_with_media("./data/media/default.png",status='@' + tweet_screen_user, in_reply_to_status_id = tweet_id)
        else:
          #Responem amb la fotografia del partit.
          self.api.update_with_media(self.getPhotoDir(predicted_party_label),status='@' + tweet_screen_user, in_reply_to_status_id = tweet_id)
        
        #Prediccio d'usuaris mencionats.
        for user in users_called_processed:
          predicted_party_label = self.predict_user(user)
          #No hem pogunt determinar la ideologia de l'usuari.
          if predicted_party_label is None:
            self.api.update_with_media("./data/media/default.png",status='@' + tweet_screen_user + " para el usuario " + '@' + user, in_reply_to_status_id = tweet_id)
          else:
            #Responem amb la fotografia del partit.
            self.api.update_with_media(self.getPhotoDir(predicted_party_label),status='@' + tweet_screen_user + " para el usuario " + '@' + user, in_reply_to_status_id = tweet_id)
    
    def on_error(self, status):
      # Si succeix un error.
      print("Error detected")

def main():

    api = create_api() # Creem la api de twitter.

    # Obtenim el nostre nom d'usuari.
    screen_user = api.me().screen_name
    print("Current user in credentials: @"+screen_user)

    # Creem un listener per trackejar els usuaris que ens mencionin.
    tweets_listener = PolitikeoStreamer(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=[screen_user]) # Trackejem amb un stream el nostre nom d'usuari.

if __name__ == "__main__":
    main()