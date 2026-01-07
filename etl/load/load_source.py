from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv('/Users/amineouhiba/Desktop/streaming-bi-project/config/db_config.env')

PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")

engine = create_engine(
    f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'
)

base_path = Path('/Users/amineouhiba/Desktop/streaming-bi-project')

df_movies = pd.read_csv(base_path / "data/source/movies.csv")
df_users = pd.read_csv(base_path / "data/source/users.csv")
df_watch = pd.read_csv(base_path / "data/source/watch_logs.csv")

df_movies = df_movies.rename(columns={'genre_ids': 'genre'})

df_movies.to_sql('movie', engine, if_exists='append', index=False, method='multi')

df_users.to_sql('users', engine, if_exists='append', index=False, method='multi')

dates = pd.DataFrame(df_watch['date'].unique(), columns=['date'])
dates['day'] = pd.to_datetime(dates['date']).dt.day
dates['month'] = pd.to_datetime(dates['date']).dt.month
dates['year'] = pd.to_datetime(dates['date']).dt.year
dates['weekday'] = pd.to_datetime(dates['date']).dt.day_name()
dates.to_sql('date_dim', engine, if_exists='append', index=False, method='multi')

date_ids = pd.read_sql("SELECT date_id, date FROM date_dim", engine)
df_watch = df_watch.merge(date_ids, on='date', how='left', validate='m:1')

df_views = df_watch[['user_id', 'movie_id', 'date_id', 'duration_minutes']]
df_views.to_sql('views', engine, if_exists='append', index=False, method='multi')

from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv("config/db_config.env")
engine = create_engine(os.getenv("DB_URL"))


    

