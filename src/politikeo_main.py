import tweepy
import json
import numpy as np
from config import create_api
import time
import sys

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
    if( len(sys.argv) < 2 ): screen_user = '@dacima_upf'
    screen_user = sys.argv[1]
    api = create_api()
    tweets_listener = PolitikeoStreamer(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=[screen_user])
    

if __name__ == "__main__":
    main()