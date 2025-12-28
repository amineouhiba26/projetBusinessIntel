import requests
import pandas as pd

baseUrl = "https://api.themoviedb.org/3/"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMzY2YjliNjkwZWJmMWJmOWEyMWFkZWU2MzNjYTVlNyIsIm5iZiI6MTc1ODA3NTY1MC42NjIwMDAyLCJzdWIiOiI2OGNhMWIwMmUxMzYyNDI1MmQ2ODMyZTQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.WgrY6oZygqxENfB0i2dbjy_9ZDPcoCz_KDOR_QIRXiY"
}


movies = []

for page in range(40, 70): 
    url = f"{baseUrl}/movie/popular"
    params = {
        "language": "en-US",
        "page": page
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for m in data["results"]:
        movies.append({
            "movie_id": m["id"],
            "title": m["title"],
            "year": m["release_date"][:4] if m["release_date"] else None,
            "genre_ids": ",".join(map(str, m["genre_ids"]))
        })

df_movies = pd.DataFrame(movies)
df_movies.to_csv("movies.csv", index=False)

