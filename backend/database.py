import mysql.connector
from mysql.connector import Error


def get_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=8889,             # MAMP default MySQL port
            user="root",
            password="root",
            database="spotify_churn"
        )
        if conn.is_connected():
            print("✅ Connected to MySQL database 'spotify_churn'")
            return conn
        else:
            print("❌ Connection failed for unknown reason")
            return None
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None


# if __name__ == "__main__":
#     connection = get_db()
#     if connection:
#         connection.close()
