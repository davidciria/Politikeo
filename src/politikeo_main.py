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
from datetime import datetime, timedelta
#Download nltk stopwords.
if 'stopwords' not in os.listdir( nltk.data.find("corpora") ):
  nltk.download('stopwords')

class PolitikeoStreamer(tweepy.StreamListener):
    def __init__(self, api):
      self.api = api
      self.me = api.me()
      self.log = self.load_log()

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
      if (decisionModelScores[0][0] >= 0.20) and (2*decisionModelScores[1][0] <= decisionModelScores[0][0]):
        #Retornem el partit politic.
        print("DecisionModelPrediction for @"+screen_user)
        print(decisionModelScores)
        print("\n")
        return decisionModelScores[0][1]
      else:
        #Apliquem fasttext.
        fastTextModel = FastTextModel(screen_user, self.api)
        fastTextModelScores = fastTextModel.getScores()
        fastTextModelScores.sort(key=lambda tup: tup[1], reverse=True)
        print("FasttextPrediction for @"+screen_user)
        print(fastTextModelScores)
        print("\n")
        #Si el score de fasttext es major del 40%, retornem la prediccio.
        if(fastTextModelScores[0][1] >= 0.4):
          return re.sub(r"__label__", "", fastTextModelScores[0][0])
        else:
          #No hem estat capaços de preedir el partit.
          return None

    def getPhotoDir(self, partyLabel):
      parties_photos = {"vox": "./data/media/vox.png", "pp": "./data/media/pp.png", "cs": "./data/media/cs.png", "psoe": "./data/media/psoe.png", "up": "./data/media/up.png"}
      return parties_photos[partyLabel]

    def load_log(self):
      if os.path.isfile('./data/log.txt'):
        log_file = open('./data/log.txt', 'r')
        lines = log_file.readlines()
        user_log_dict = {}
        for line in lines:
            user, time = line.strip().split(",")
            user_log_dict[user] = time
        return user_log_dict
      else:
        return {}

    def save_log(self):
      log_file = open('./data/log.txt', 'w')
      for user in self.log:
        log_file.write(user+","+self.log[user]+"\n")
      return True
    
    def user_allowed(self, tweet_screen_user):
      if tweet_screen_user in self.log:
        last_time_str = self.log[tweet_screen_user]
        last_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.now()
        if ((now - last_time) >= timedelta(hours=1)):
          self.log[tweet_screen_user] = str(now)
          self.save_log() #Update log.
          return True
        else:
          return False
      else:
        now = datetime.now()
        self.log[tweet_screen_user] = str(now)
        self.save_log()
        return True

    def on_status(self, tweet):
      # Informacio del tweet que ens ha mencionat.
      tweet_id = tweet.id
      tweet_screen_user = tweet.user.screen_name
      if tweet.user.screen_name.lower() != self.me.screen_name.lower(): #and self.user_allowed(tweet_screen_user.lower()):
        users_called = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-.]))@([A-Za-z0-9-_]+)', tweet.text)
        users_called_processed = [u for u in list(set(users_called)) if u!=tweet.user.screen_name and u!=self.me.screen_name]  #Eliminem duplicats i obtenim usuaris diferents.
        # Processament dels usuaris que ha mencionat.
        if len(users_called_processed) >= 1:
          #Prediccio d'usuaris mencionats.
          for user in users_called_processed:
            predicted_party_label = self.predict_user(user)
            #No hem pogunt determinar la ideologia de l'usuari.
            if predicted_party_label is None:
              self.api.update_with_media("./data/media/default.png",status='@' + tweet_screen_user + " Nuestra prediccion para el usuario " + '@/' + user, in_reply_to_status_id = tweet_id)
            else:
              #Responem amb la fotografia del partit.
              self.api.update_with_media(self.getPhotoDir(predicted_party_label),status='@' + tweet_screen_user + " Nuestra prediccion para el usuario " + '@/' + user, in_reply_to_status_id = tweet_id)
        else: # Processament del partit politic del usuari que ha mencionat el bot.
          predicted_party_label = self.predict_user(tweet_screen_user)

          #No hem pogunt determinar la ideologia de l'usuari.
          if predicted_party_label is None:
            self.api.update_with_media("./data/media/default.png",status='@' + tweet_screen_user, in_reply_to_status_id = tweet_id)
          else:
            #Responem amb la fotografia del partit.
            self.api.update_with_media(self.getPhotoDir(predicted_party_label),status='@' + tweet_screen_user, in_reply_to_status_id = tweet_id)
          
    
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