"""

FastAPI Backend for Sentiment Trends.
This exposes APIs for React frontend to fetch data.

"""

from fastapi import FastAPI
from database import get_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.get("/sentiment_score")
def get_sentiment_score():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(sentiment_score) FROM sentiment WHERE date >= NOW() - INTERVAL '1 day'")
    avg_score = cursor.fetchone()[0]
    conn.close()
    return {"sentiment_score": avg_score if avg_score is not None else 0}

@app.get("/sentiment_trend.{period}")
def get_sentiment_trend(period: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    if period == "weekly":
        cursor.execute("SELECT data::DATE, AVG(sentiment_score) FROM sentiment WHERE date >- NOW() - INTERVAL '7 days' GROUP BY date::DATE")
    elif period == "monthly":
        cursor.execute("SELECT date_trunc('month', date) AS month, AVG(sentiment_score) FROM sentiment WHERE date >= NOW() - INTERVAL '1 month' GROUP BY month")
    elif period == "yearly":
        cursor.execute("SELECT date_trunc('year', date) AS year, AVG(sentiment_score) FROM sentiment WHERE date >= NOW() - INTERVAL '1 year' GROUP BY year")
    else:
        return {"error": "Invalid period. Use 'weekly', 'monthly', or 'yearly'."}

    trend_data = cursor.fetchall()
    conn.close()

    return [{"date": row[0], "sentiment_score": row[1]} for row in trend_data]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
