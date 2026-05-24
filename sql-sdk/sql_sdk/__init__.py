from typing import Any

__version__ = "0.0.1"

__all__ = ["sql"]

def get_provider_info() -> dict[str, Any]:
    return {
        "package-name": "sql-sdk",
        "name": "SQL SDK",
        "description": "SQL SDK is package that provide set of tools to work with Airflow DAGs",
        "version": __version__,
        "task-decorators": [
            {
                "name": "sql",
                "class-name": "sql_sdk.decorators.sql.sql_task"
            }
        ]
    }