from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

# Charger config
load_dotenv('/Users/amineouhiba/Desktop/streaming-bi-project/config/db_config.env')

PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")

engine = create_engine(
    f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'
)

# Dossier export
export_path = Path('/Users/amineouhiba/Desktop/streaming-bi-project/data/export')
export_path.mkdir(exist_ok=True)

# Exporter dimensions
pd.read_sql("SELECT * FROM dim_movie", engine).to_csv(export_path / "dim_movie.csv", index=False)
pd.read_sql("SELECT * FROM dim_user", engine).to_csv(export_path / "dim_user.csv", index=False)
pd.read_sql("SELECT * FROM dim_date", engine).to_csv(export_path / "dim_date.csv", index=False)

# Exporter faits
pd.read_sql("SELECT * FROM fact_views", engine).to_csv(export_path / "fact_views.csv", index=False)

print("✅ Export CSV terminé, fichiers prêts pour Power BI.")
