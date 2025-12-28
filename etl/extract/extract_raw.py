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

# Connexion - remove future parameter
engine = create_engine(
    f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'
)

def extract():
    return {
        "movies": pd.read_sql("SELECT * FROM movie", engine),
        "users": pd.read_sql("SELECT * FROM users", engine),
        "views": pd.read_sql("SELECT * FROM views", engine),
        "dates": pd.read_sql("SELECT * FROM date_dim", engine)
    }
