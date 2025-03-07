"""

This script:
- scrapes tweets from the past 1 year.
- performs sentiment analysis using VADER
- Stores data in PostgreSQL

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