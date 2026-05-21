
from airflow.sdk import asset, Asset, Context

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


# second asset, take location from user
# this will run after the `user` asset materialized
@asset(
    schedule = user
)
def user_location(user: Asset, context: Context) -> dict[str]:

    # if not user or "results" not in user:
    #     return {}
    
    user_data = context['ti'].xcom_pull(
        dag_id = user.name,
        task_ids = user.name,
        # latest user asset
        include_prior_dates = True
    )

    if not user_data or "results" not in user_data[-1]:
    # if not user_data or "results" not in user_data[-1]:
        print("ERRROR EXIT.....")
        return {}

    return user_data[-1]["results"][0]["location"]
    # return user_data[-1]["results"][0]["location"]

