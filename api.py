"""

FastAPI Backend for Sentiment Trends.
This exposes APIs for React frontend to fetch data.

"""

from fastapi import FastAPI
from database import get_db_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

@app.get("/sentiment_score")
def get_sentiment_score(timeframe: str = "day"):
    conn = get_db_connection()
    cursor = conn.cursor()

    query_map = {
        "day": "1 day",
        "week": "7 days",
        "month": "1 month",
        "year": "1 year"
    }
    interval = query_map.get(timeframe, "1 day")

    cursor.execute(f"SELECT AVG(sentiment_score) FROM sentiment WHERE date >= NOW() - INTERVAL '{interval}'")
    result = cursor.fetchone()
    conn.close()
    return {"sentiment_score": result[0] if result[0] is not None else 0}

@app.get("/sentiment_trend")
def get_sentiment_trend(timeframe: str = "week"):
    # Group by date and calculate average sentiment per day
    conn = get_db_connection()
    cursor = conn.cursor()
    query_map = {
        "day": "1 day",
        "week": "7 days",
        "month": "1 month",
        "year": "1 year"
    }
    interval = query_map.get(timeframe, "7 days")

    cursor.execute(f"""
        SELECT DATE(date) as day, AVG(sentiment_score)
        FROM sentiment
        WHERE date >= NOW() - INTERVAL %s
        GROUP BY day
        ORDER BY day ASC
    """, (interval,))
    rows = cursor.fetchall()
    conn.close()
    return [{"date": str(row[0]), "index": round(row[1]*100, 2)} for row in rows]


@app.get("/top_reddit_posts")
def get_top_reddit_posts(limit: int = 5):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tweet, sentiment_score, date
        FROM sentiment
        ORDER BY sentiment_score DESC
        LIMIT %s
    """, (limit,))
    posts = cursor.fetchall()
    conn.close()
    return [
        {
            "text": post[0][:200] + ("..." if len(post[0]) > 200 else ""),
            "score": round(post[1], 2),
            "date": post[2].strftime("%Y-%m-%d")
        }
        for post in posts
    ]

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
    uvicorn.run(app, host="0.0.0.0", port=8000)"""
