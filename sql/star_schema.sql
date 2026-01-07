CREATE TABLE IF NOT EXISTS dim_movie (
    movie_id INT PRIMARY KEY,
    title TEXT,
    genre TEXT,
    release_year INT
);

CREATE TABLE IF NOT EXISTS dim_user (
    user_id INT PRIMARY KEY,
    gender TEXT,
    country TEXT,
    age_group TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT PRIMARY KEY,
    date DATE,
    day INT,
    month INT,
    year INT,
    weekday TEXT
);

CREATE TABLE IF NOT EXISTS fact_views (
    movie_id INT,
    user_id INT,
    date_id INT,
    total_watch_time INT,
    total_views INT,
    is_long_view INT,
    PRIMARY KEY (movie_id, user_id, date_id),
    FOREIGN KEY (movie_id) REFERENCES dim_movie(movie_id),
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);
