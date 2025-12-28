from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

import os
from dotenv import load_dotenv

# Charger config
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


def load(data):
    with engine.begin() as conn:
        # vider les tables
        conn.execute(text("TRUNCATE TABLE fact_views CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_movie CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_user CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_date CASCADE;"))

        # charger les données
        data["dim_movie"].to_sql("dim_movie", conn, if_exists="append", index=False)
        data["dim_user"].to_sql("dim_user", conn, if_exists="append", index=False)
        data["dim_date"].to_sql("dim_date", conn, if_exists="append", index=False)
        data["fact_views"].to_sql("fact_views", conn, if_exists="append", index=False)