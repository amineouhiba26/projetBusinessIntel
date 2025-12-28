import pandas as pd

def transform(data):
    df_movies = data["movies"].drop_duplicates("movie_id")
    df_movies["genre"] = df_movies["genre"].str.lower().str.strip()
    df_movies = df_movies[df_movies["year"] > 1900]

    df_users = data["users"].drop_duplicates("user_id")
    df_views = data["views"]
    df_dates = data["dates"].drop_duplicates("date_id") # Deduplicate dates
    
    # Handle missing date_id in views
    # Fill NaN with -1
    df_views["date_id"] = df_views["date_id"].fillna(-1).astype(int)
    
    # Ensure date_id -1 exists in df_dates
    if -1 not in df_dates["date_id"].values:
        unknown_date = pd.DataFrame([{
            "date_id": -1,
            "date": pd.to_datetime("1900-01-01"),
            "day": 1,
            "month": 1,
            "year": 1900,
            "weekday": "Unknown"
        }])
        df_dates = pd.concat([df_dates, unknown_date], ignore_index=True)

    # Create a mapping from UUID to integer for user_id
    # Use all unique user_ids from both users and views to ensure complete mapping
    all_user_ids = pd.concat([df_users["user_id"], df_views["user_id"]]).unique()
    user_id_mapping = {uuid: idx + 1 for idx, uuid in enumerate(all_user_ids)}
    
    # Filter and transform users
    df_users = df_users[(df_users["age"] >= 10) & (df_users["age"] <= 100)]
    df_users["country"] = df_users["country"].fillna("Unknown")
    
    # Map UUID to integer
    df_users["user_id_original"] = df_users["user_id"]
    df_users["user_id"] = df_users["user_id"].map(user_id_mapping)

    df_users["age_group"] = pd.cut(
        df_users["age"],
        bins=[0,18,30,45,60,100],
        labels=["<18","18-30","30-45","45-60","60+"]
    ).astype(str) # Ensure string type for SQL

    # Map user_id in views to the integer mapping
    df_views["user_id"] = df_views["user_id"].map(user_id_mapping)
    # Filter out views for users that were filtered out (age restriction)
    df_views = df_views[df_views["user_id"].isin(df_users["user_id"])]
    # Filter out views for movies that were filtered out (year restriction)
    df_views = df_views[df_views["movie_id"].isin(df_movies["movie_id"])]
    
    df_views["user_id"] = df_views["user_id"].astype(int)
    
    df_views["is_long_view"] = df_views["duration_minutes"].apply(
        lambda x: 1 if x >= 60 else 0
    )

    fact_views = (
        df_views
        .groupby(["movie_id", "user_id", "date_id"])
        .agg(
            total_watch_time=("duration_minutes", "sum"),
            total_views=("duration_minutes", "count"),
            is_long_view=("is_long_view", "max")
        )
        .reset_index()
    )

    return {
        "dim_movie": df_movies[["movie_id","title","genre","year"]].rename(columns={"year": "release_year"}),
        "dim_user": df_users[["user_id","country","age_group"]],
        "dim_date": df_dates,
        "fact_views": fact_views
    }
