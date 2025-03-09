"""

This script:
- scrapes tweets from the past 1 year.
- performs sentiment analysis using VADER
- Stores data in PostgreSQL

"""
import tweepy
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from database import get_db_connection

# 🔑 Replace these with your actual API credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Sentiment Analysis Function
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)["compound"]

# Scrape and Analyze Tweets
def scrape_tweets():
    query = "#Sustainability OR #ClimateAction OR #RenewableEnergy OR #NetZero OR #ESG OR #GreenTech OR #CarbonNeutral OR #ClimateCrisis OR #EcoFriendly -filter:retweets"
    tweets_data = []

    # Get tweets from the past day
    since_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="en", since=since_date, count=100).items(500):  # Fetch up to 500 tweets
        score = analyze_sentiment(tweet.text)
        tweets_data.append((tweet.created_at, tweet.text, score))

    # Store in PostgreSQL
    if tweets_data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO sentiment (date, tweet, sentiment_score) VALUES (%s, %s, %s)", tweets_data)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Successfully stored {len(tweets_data)} tweets in the database.")
    else:
        print("⚠️ No new tweets found.")

# Run Scraper
if __name__ == "__main__":
    scrape_tweets()



"""

import snscrape.modules.twitter as sntwitter
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from database import get_db_connection

# Sentiment Analysis Function
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)["compound"]

# Scrape and Analyze Tweets
def scrape_tweets():
    query = """
    (#Sustainability OR #ClimateAction OR #RenewableEnergy OR #NetZero OR 
    #ESG OR #GreenTech OR #CarbonNeutral OR #ClimateCrisis OR #EcoFriendly) 
    since:2023-03-01 until:2024-03-01
    """
    tweets_data = []

    for tweet in sntwitter.TwitterSearchScraper(f"{query}").get_items():
        score = analyze_sentiment(tweet.content)
        tweets_data.append((tweet.date, tweet.content, score))


    # Store in PostgreSQL
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO sentiment (date, tweet, sentiment_score) VALUES (%s, %s, %s)", tweets_data)
    conn.commit()
    cursor.close()
    conn.close()

# Run Scraper
if __name__ == "__main__":
    scrape_tweets()
    
    """