import tweepy
import json
import numpy as np
from config import create_api
import time

class PolitikeoStreamer(tweepy.StreamListener):
    def __init__(self, api):
      self.api = api
      self.me = api.me()

    def on_status(self, tweet):
      # Informacio del tweet que ens ha mencionat.
      tweet_id = tweet.id
      tweet_scrren_user = tweet.user.screen_name
      
      # Processament del partit politic del usuari.
      # TO DO
      img_partit = 'prova.jpg'

      # Resposta del tweet amb la imatge resultant.
      self.api.update_with_media(img_partit,status='hello world'+' @'+tweet.user.screen_name, in_reply_to_status_id = tweet.id)

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