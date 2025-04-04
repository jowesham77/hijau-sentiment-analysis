"""

Render supports PostgreSQL so we store tweets and sentiment scores there.
Here, we are creating and connecting to PostgreSQL using environment variables
for security.
PostgreSQL is always used.

"""
import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(os.environ["postgresql://hijau_sentiment0sql_user:II3PvqlGzGhpZjYkLPATDZho22CIRmwc@dpg-cv53d8a3esus73aoghug-a.oregon-postgres.render.com/hijau_sentiment0sql"])

"""import psycopg2
import os

DB_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DB_URL, sslmode = "require")

def create_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS sentiment(
                   id SERIAL PRIMARY KEY,
                   date TIMESTAMP,
                   tweet TEXT,
                   sentiment_score REAL
                   )''')
    conn.commit()
    cursor.close()
    conn.close()"""