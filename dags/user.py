
from airflow.sdk import asset

@asset(
    schedule = "@daily",
    uri = "https://randomuser.me/api",
    # uri = "https://randomuser.me/api?results=5"
)
def user(self) -> dict[str]:
    import requests

    req = requests.get(self.uri)
    if req.status_code == 200:
        return req.json()
    return None