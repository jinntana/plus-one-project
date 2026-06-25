import psycopg2
from db.credentials import DB_NAME

def get_connection():
    conn = psycopg2.connect(dbname=DB_NAME)

    return conn


if __name__ == "__main__":
    conn = get_connection()
    print("Connected to database")
    conn.close()