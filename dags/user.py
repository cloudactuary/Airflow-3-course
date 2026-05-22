
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


@asset.multi(
    schedule = user,
    outlets = [
        Asset(name = "user_location"),
        Asset(name = "user_login"),
    ]
)
def user_info_asset(user: Asset, context: Context) -> list[dict[str]]:
    user_data = context['ti'].xcom_pull(
        dag_id = user.name,
        task_ids = user.name,
        # latest user asset
        include_prior_dates = True
    )

    return [
        user_data[-1]["results"][0]["location"],
        user_data[-1]["results"][0]["login"],
    ]