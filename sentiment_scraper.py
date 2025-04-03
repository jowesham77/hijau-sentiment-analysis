"""

This script:
- scrapes tweets from the past 1 year.
- performs sentiment analysis using VADER
- Stores data in PostgreSQL

"""

import praw
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from database import get_db_connection
from datetime import datetime, timezone
import time

# === CONFIG ===
REDDIT_CLIENT_ID = "xMgGYXP3LJNxJMtyc6nH5Q"
REDDIT_CLIENT_SECRET = "9guCl-kSpRTMrvygTWBQLRUUWMnw9A"
REDDIT_USER_AGENT = "ProfessionalBill5616"

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)["compound"]

def scrape_reddit(historical=False):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    subreddits = ["sustainability", "climate", "renewableenergy"]
    posts_data = []
    one_day_ago = time.time() - (24 * 60 * 60)  # UNIX time for 24 hours ago
    seen_titles = set()

    for subreddit in subreddits:
        posts = reddit.subreddit(subreddit).hot(limit=500) if historical else reddit.subreddit(subreddit).new(limit=100)

        for post in posts:
            post_time = post.created_utc
            if not historical and post_time < one_day_ago:
                continue  # Skip older posts if we're doing daily

            full_text = post.title + " " + post.selftext

            if post.title in seen_titles:
                continue
            seen_titles.add(post.title)

            dt = datetime.fromtimestamp(post_time, tz=timezone.utc)
            score = analyze_sentiment(full_text)
            posts_data.append((dt, post.title, score))

    if posts_data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO sentiment (date, tweet, sentiment_score) VALUES (%s, %s, %s)", posts_data)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Stored {len(posts_data)} Reddit posts.")
    else:
        print("⚠️ No new Reddit posts found.")

if __name__ == "__main__":
    # Run historical collection ONCE
    scrape_reddit(historical=True)

    # Run these daily
    scrape_reddit(historical=False)



"""
import tweepy
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from database import get_db_connection

# 🔑 API credentials
API_KEY = "dvpDt97al6NlSQnwC9u1rxMNn"
API_SECRET = "wxeRfbL8AvCWcycgOdcNbEU6BJe1JhLOr0juEoRLY6jMjrMYsz"
ACCESS_TOKEN = "998204003505729537-3ywhLfqgznHXUjxp2saIm2h5lhfyhFE"
ACCESS_SECRET = "8hjRzHvd8rN3lU6zYti9k91sDCq2P586HjIsyLuvyn6ak"

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




if use snscrape:

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
    query = 
    (#Sustainability OR #ClimateAction OR #RenewableEnergy OR #NetZero OR 
    #ESG OR #GreenTech OR #CarbonNeutral OR #ClimateCrisis OR #EcoFriendly) 
    since:2023-03-01 until:2024-03-01
    
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