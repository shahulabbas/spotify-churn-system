import random
from database import get_db


def insert_user():
    db = get_db()
    cur = db.cursor()

    query = """
    INSERT INTO users 
    (subscription_type, age, country, avg_listening_hours_per_week,
     login_frequency_per_week, songs_skipped_per_week,
     playlists_created, days_since_last_login, churn)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    data = (
        random.choice(["Free", "Premium"]),
        random.randint(18, 50),
        random.choice(["India", "USA", "UK"]),
        random.uniform(1, 40),
        random.randint(1, 14),
        random.randint(0, 50),
        random.randint(0, 20),
        random.randint(0, 60),
        random.choice([0, 1])
    )

    cur.execute(query, data)
    db.commit()
    db.close()
