# src/config.py
import os
import logging
import tweepy

logger = logging.getLogger()

def create_api():
    #Funcio per llegir les keys del fitxer api_keys.txt que ha d'estar situat al directori data.
    def load_keys():
      if os.path.isfile('./data/api_keys.txt'):
        log_file = open('./data/api_keys.txt', 'r')
        lines = log_file.readlines()
        keys_dict = {}
        for line in lines:
            key, value = line.strip().split(",")
            keys_dict[key] = value
        return keys_dict
      else:
        print("Create api_keys.txt file in data directory")
        print("The format should be the following:")
        print("consumer_key,insert_here_your_consumer_key")
        print("consumer_secret,insert_here_your_consumer_secret")
        print("access_token,insert_here_your_access_token")
        print("access_token_secret,insert_here_your_access_token_secret")
        return {}

    keys_dict = load_keys()
    consumer_key = keys_dict["consumer_key"]
    consumer_secret = keys_dict["consumer_secret"]
    access_token = keys_dict["access_token"]
    access_token_secret = keys_dict["access_token_secret"]
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api