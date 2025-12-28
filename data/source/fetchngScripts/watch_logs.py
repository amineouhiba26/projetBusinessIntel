import pandas as pd
import random
from datetime import datetime, timedelta

movies = pd.read_csv("movies.csv")
users = pd.read_csv("users.csv")

watch_logs = []

for i in range(5000):  # 5000 visionnages
    user = users.sample(1).iloc[0]
    movie = movies.sample(1).iloc[0]

    watch_logs.append({
        "watch_id": i + 1,
        "user_id": user["user_id"],
        "movie_id": movie["movie_id"],
        "date": (datetime.now() - timedelta(days=random.randint(0, 180))).date(),
        "duration_minutes": random.randint(20, 180)
    })

df_watch = pd.DataFrame(watch_logs)
df_watch.to_csv("watch_logs.csv", index=False)

print("✔ watch_logs.csv généré")
