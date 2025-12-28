import requests
import pandas as pd

users = []
url = "https://randomuser.me/api/"

for i in range(8): 
    params = {
        "results": 100,
        "nat": "us,fr,de,es,it"
    }
    response = requests.get(url, params=params)
    data = response.json()

    for u in data["results"]:
        users.append({
            "user_id": u["login"]["uuid"],
            "name": f"{u['name']['first']} {u['name']['last']}",
            "age": u["dob"]["age"],
            "country": u["location"]["country"]
        })

df_users = pd.DataFrame(users)
df_users.to_csv("users.csv", index=False)

