CREATE TABLE movie (
    movie_id BIGINT PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT,
    year INT
);

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT,
    country TEXT
);

CREATE TABLE date_dim (
    date_id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    day INT,
    month INT,
    year INT,
    weekday TEXT
);

CREATE TABLE views (
    view_id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id),
    movie_id BIGINT REFERENCES movie(movie_id),
    date_id INT REFERENCES date_dim(date_id),
    duration_minutes INT
);
