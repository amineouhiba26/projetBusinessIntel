# 🎬 Streaming Platform Business Intelligence Project

## 📋 Project Overview

This project implements a complete **ETL (Extract, Transform, Load) pipeline** and **Data Warehouse** solution for a streaming platform, enabling advanced business intelligence analytics. The solution follows a **star schema** design pattern optimized for analytical queries and visualization in Power BI.

### Key Objectives 
- Build a scalable data warehouse for streaming analytics
- Implement automated ETL processes
- Enable data-driven decision making through BI dashboards
- Track user behavior, content performance, and viewing patterns

---

## 🏗️ Architecture

### Technology Stack
- **Database**: PostgreSQL
- **ETL Framework**: Python (pandas, SQLAlchemy)
- **Data Sources**: TMDB API, synthetic user data
- **BI Tool**: Power BI
- **Configuration**: Environment variables (.env)

### Data Flow
```
[External APIs] → [Raw Data CSVs] → [Source Tables] → [ETL Pipeline] → [Star Schema DW] → [Power BI]
```

---

## 📊 Data Model - Star Schema

### Dimension Tables

#### 1. **dim_movie**
- `movie_id` (PK): Unique movie identifier
- `title`: Movie title
- `genre`: Movie genre
- `release_year`: Year of release

#### 2. **dim_user**
- `user_id` (PK): Unique user identifier (integer mapping from UUID)
- `country`: User's country
- `age_group`: Categorized age range (<18, 18-30, 30-45, 45-60, 60+)

#### 3. **dim_date**
- `date_id` (PK): Unique date identifier
- `date`: Actual date
- `day`, `month`, `year`: Date components
- `weekday`: Day of the week

### Fact Table

#### **fact_views**
- `movie_id` (FK): Reference to dim_movie
- `user_id` (FK): Reference to dim_user
- `date_id` (FK): Reference to dim_date
- `total_watch_time`: Aggregated viewing duration (minutes)
- `total_views`: Number of views
- `is_long_view`: Boolean flag for views ≥ 60 minutes

---

## 🔧 Project Setup - Step by Step

### Step 1: Environment Setup

1. **Install Dependencies**
   ```bash
   pip install pandas sqlalchemy psycopg2-binary python-dotenv requests
   ```

2. **Configure Database Connection**
   - Edit `/config/db_config.env`:
   ```env
   PGHOST=localhost
   PGPORT=5432
   PGDATABASE=streaming_db
   PGUSER=postgres
   PGPASSWORD=your_password
   ```

### Step 2: Database Initialization

1. **Create Database Schema**
   ```bash
   # Create source tables
   psql -U postgres -d streaming_db -f sql/create_tables.sql
   
   # Create data warehouse star schema
   psql -U postgres -d streaming_db -f sql/star_schema.sql
   ```

2. **Tables Created**:
   - Source: `movie`, `users`, `date_dim`, `views`
   - Warehouse: `dim_movie`, `dim_user`, `dim_date`, `fact_views`

### Step 3: Data Generation

1. **Fetch Movie Data from TMDB API**
   ```bash
   cd data/source/fetchngScripts
   python films.py
   ```
   - Fetches 600 popular movies (pages 40-70)
   - Generates `movies.csv` with movie details

2. **Generate Synthetic User Data**
   ```bash
   python users.py
   ```
   - Creates realistic user profiles
   - Generates `users.csv` with demographics

3. **Generate Watch Logs**
   ```bash
   python watch_logs.py
   ```
   - Creates 5,000 viewing records
   - Simulates 180 days of streaming activity
   - Generates `watch_logs.csv`

### Step 4: Load Source Data

1. **Populate Source Tables**
   - Load CSVs into PostgreSQL source tables
   - Creates date dimension from watch logs
   - Establishes referential integrity

### Step 5: ETL Pipeline Execution

1. **Run ETL Pipeline**
   ```bash
   cd etl
   python etl_pipeline.py
   ```

#### ETL Process Breakdown:

**EXTRACT Phase** (`extract/extract_raw.py`):
- Connects to PostgreSQL using SQLAlchemy
- Extracts data from source tables (movie, users, views, date_dim)
- Returns raw data as pandas DataFrames

**TRANSFORM Phase** (`transform/transform_dw.py`):
- **Data Quality**:
  - Removes duplicate records
  - Filters invalid years (year > 1900)
  - Validates user ages (10-100 years)
  - Handles missing values (country → "Unknown")
  
- **Data Standardization**:
  - Normalizes genres (lowercase, trimmed)
  - Maps UUID user IDs to integers
  - Creates age groups using binning
  
- **Business Logic**:
  - Flags long views (≥ 60 minutes)
  - Handles missing date_id with placeholder (-1)
  - Ensures referential integrity
  
- **Aggregation**:
  - Groups views by (movie, user, date)
  - Calculates total watch time
  - Counts total views per combination

**LOAD Phase** (`load/load_dw.py`):
- Truncates existing warehouse tables
- Loads transformed dimensions
- Loads aggregated fact table
- Uses database transactions for consistency

### Step 6: Export for Power BI

1. **Generate CSV Exports**
   ```bash
   python export_csv.py
   ```
   - Exports all dimension and fact tables to `/data/export/`
   - Creates Power BI-ready CSV files:
     - `dim_movie.csv`
     - `dim_user.csv`
     - `dim_date.csv`
     - `fact_views.csv`

### Step 7: Power BI Integration

1. **Import Data**
   - Load CSV files into Power BI Desktop
   - Establish relationships matching star schema
   
2. **Create Visualizations**
   - Build dashboards for KPIs
   - Analyze viewing trends
   - Track user engagement metrics

---

## 📁 Project Structure

```
streaming-bi-project/
├── config/
│   └── db_config.env           # Database connection settings
├── data/
│   ├── source/                 # Raw data sources
│   │   ├── movies.csv
│   │   ├── users.csv
│   │   ├── watch_logs.csv
│   │   └── fetchngScripts/     # Data generation scripts
│   │       ├── films.py        # TMDB API fetcher
│   │       ├── users.py        # User data generator
│   │       └── watch_logs.py   # Viewing log generator
│   ├── export/                 # Power BI ready exports
│   │   ├── dim_movie.csv
│   │   ├── dim_user.csv
│   │   ├── dim_date.csv
│   │   └── fact_views.csv
│   ├── staging/                # Intermediate processing
│   └── warehouse/              # Final transformed data
├── etl/
│   ├── etl_pipeline.py         # Main ETL orchestrator
│   ├── export_csv.py           # Data warehouse export
│   ├── extract/
│   │   └── extract_raw.py      # Extract from source DB
│   ├── transform/
│   │   └── transform_dw.py     # Transform & aggregate
│   └── load/
│       ├── load_dw.py          # Load to data warehouse
│       └── load_source.py      # Load raw data to source
├── sql/
│   ├── create_tables.sql       # Source table schemas
│   ├── star_schema.sql         # Data warehouse schemas
│   ├── drop_tables.sql         # Cleanup scripts
│   └── indexes.sql             # Performance optimization
├── scripts/
│   └── fix_views_date_id.py    # Data quality fixes
├── powerbi/
│   └── screenshots/            # BI dashboard images
└── README.md                   # This file
```

---

## 🔍 Key Features & Insights

### Data Quality Management
- **Deduplication**: Removes duplicate records across all dimensions
- **Validation**: Age ranges, year constraints, referential integrity
- **Missing Data Handling**: Default values for unknowns
- **Type Conversion**: UUID to integer mapping for performance

### Business Rules Implemented
1. **Age Groups**: Demographic segmentation for targeted analysis
2. **Long View Classification**: Engagement metric (60+ minutes)
3. **Date Dimension**: Time-based analysis capabilities
4. **Aggregated Facts**: Pre-calculated metrics for performance

### Performance Optimizations
- Star schema design for query efficiency
- Aggregated fact table reduces data volume
- Integer keys for faster joins
- Transaction-based loading for data consistency

---

## 📈 Analytical Use Cases

This data warehouse enables analysis of:

1. **Content Performance**
   - Most watched movies
   - Genre popularity trends
   - Seasonal viewing patterns

2. **User Behavior**
   - Engagement by age group
   - Geographic viewing preferences
   - Binge-watching patterns

3. **Platform Metrics**
   - Total viewing hours
   - Active user counts
   - Content catalog utilization

4. **Temporal Analysis**
   - Day-of-week trends
   - Monthly growth patterns
   - Peak viewing times

---

## 🚀 Running the Complete Pipeline

Execute the full pipeline in order:

```bash
# 1. Generate source data
cd data/source/fetchngScripts
python films.py
python users.py
python watch_logs.py

# 2. Initialize database
cd ../../../
psql -U postgres -d streaming_db -f sql/create_tables.sql
psql -U postgres -d streaming_db -f sql/star_schema.sql

# 3. Load source data (manual or via load_source.py)
# ... load CSVs into source tables ...

# 4. Run ETL pipeline
cd etl
python etl_pipeline.py

# 5. Export for Power BI
python export_csv.py
```

---

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check credentials in `db_config.env`
   - Ensure database exists

2. **Missing Date IDs**
   - Run `scripts/fix_views_date_id.py`
   - Ensures all dates in views exist in date_dim

3. **User ID Mapping Issues**
   - Transform phase handles UUID → integer conversion
   - Filters orphaned records automatically

---

## 📝 Future Enhancements

- [ ] Add incremental ETL (process only new data)
- [ ] Implement data quality monitoring
- [ ] Create automated testing suite
- [ ] Add slowly changing dimensions (SCD Type 2)
- [ ] Build real-time streaming data ingestion
- [ ] Implement data lineage tracking
- [ ] Add data masking for privacy compliance
- [ ] Create API for direct Power BI connection

---

## 👥 Contributors

- **Project Type**: Business Intelligence & Data Warehousing
- **Database**: PostgreSQL
- **ETL**: Python-based pipeline
- **Visualization**: Power BI

---

## 📄 License

This project is designed for educational and analytical purposes.

---

## 🎯 Conclusion

This project demonstrates a complete end-to-end BI solution, from data generation and ETL processing to analytical data warehouse design. The star schema architecture provides a solid foundation for scalable analytics, while the Python-based ETL pipeline ensures maintainability and extensibility.

**Key Achievements**:
✅ Fully automated data pipeline  
✅ Production-ready star schema  
✅ Clean, validated data warehouse  
✅ Power BI integration ready  
✅ Modular, maintainable codebase
