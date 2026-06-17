import psycopg2
from db.credentials import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

def get_connection():
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
    )

    return conn


if __name__ == "__main__":
    conn = get_connection()
    print("Database connected successfully")
    conn.close()