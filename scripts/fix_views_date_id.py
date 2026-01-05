from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load config
load_dotenv('/Users/amineouhiba/Desktop/streaming-bi-project/config/db_config.env')

PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")

engine = create_engine(
    f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'
)

print('🔄 Fixing views table with proper date_id mapping...')

# Clear views table
with engine.begin() as conn:
    conn.execute(text('TRUNCATE TABLE views CASCADE'))
    print('✅ Cleared views table')

# Load CSV
base_path = Path('/Users/amineouhiba/Desktop/streaming-bi-project')
df_watch = pd.read_csv(base_path / 'data/source/watch_logs.csv')

print(f'📁 Loaded {len(df_watch)} watch logs from CSV')

# Get date_id mapping
date_ids = pd.read_sql('SELECT date_id, date FROM date_dim', engine)
print(f'📅 Found {len(date_ids)} dates in date_dim')

# Merge to get date_id
df_watch = df_watch.merge(date_ids, on='date', how='left', validate='m:1')

print(f'🔗 Merged watch logs with dates')
print(f'   - Rows with date_id: {df_watch["date_id"].notna().sum()}')
print(f'   - Rows without date_id: {df_watch["date_id"].isna().sum()}')

# Load views
df_views = df_watch[['user_id', 'movie_id', 'date_id', 'duration_minutes']]
df_views.to_sql('views', engine, if_exists='append', index=False, method='multi')

print(f'✅ Loaded {len(df_views)} views into database')

# Verify
with engine.connect() as conn:
    count = conn.execute(text('SELECT COUNT(*) FROM views WHERE date_id IS NOT NULL')).scalar()
    print(f'✅ Verification: {count} views with valid date_id')
