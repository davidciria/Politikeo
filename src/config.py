# src/config.py
import os
import logging
import tweepy

logger = logging.getLogger()

def create_api():
    #Variables entorn per llegir les keys.
    """
    consumer_key = "wnhgSExHjio16XRyg6Vz46ZYP"#os.getenv("CONSUMER_KEY")
    consumer_secret = "vVGBXEQMi9geU28yj4MjPS741YdEKhysTXuTAK9Ymxwdpl90bP"#os.getenv("CONSUMER_SECRET")
    access_token = "1222889545701580800-WpL4G8ZEsz5OKXkGGBmuDI60oOxLNt"#os.getenv("ACCESS_TOKEN")
    access_token_secret = "HcjGOyLbT3ETf4V2bjVaXoxGL7o15v79VvfZI2ASVYUFG"#os.getenv("ACCESS_TOKEN_SECRET")
    """
    consumer_key = "I0HQQB4aEyljovIhDWemu8N6I"#os.getenv("CONSUMER_KEY")
    consumer_secret = "NMBKJXKtD95qOJRtHXr241VkTqfcO1P9MiJXEmQKBFkrYqPFwx"#os.getenv("CONSUMER_SECRET")
    access_token = "1328431351259869184-VBQDCqEBMt9dpXKIPwXtoBgjvePP2q"#os.getenv("ACCESS_TOKEN")
    access_token_secret = "ixpIugMncCrcgQ6MF0Va9RTEwbdRtQsG7gkvz8XGQNMHi"#os.getenv("ACCESS_TOKEN_SECRET")
    
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