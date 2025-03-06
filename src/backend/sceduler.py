"""

This is Render's built-in cron job scheduler.
This ensures that tweets are collected daily at 7AM.

"""

import time
from sentiment_scraper import scrape_tweets

def run_daily():
    while True:
        current_time = time.strftime("%H:%<:%S")
        if current_time == "07:00:00":
            scrape_tweets()
        time.sleep(60)

if __name__ == "__main__":
    run_daily()