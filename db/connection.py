import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
    )

    return conn


if __name__ == "__main__":
    conn = get_connection()
    print("Connected to database")
    conn.close()