import pandas as pd
from database import get_db

db = get_db()
df = pd.read_sql("SELECT * FROM users", db)
df.to_csv("spotify_users.csv", index=False)
