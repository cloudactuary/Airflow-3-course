# Airflow 3 Course Project

This repository is dedicated to exploring and mastering **Apache Airflow 3**. It contains practical examples, DAG implementations, and a custom Airflow Provider (SQL SDK) designed to showcase the new features and architectural changes in Airflow 3.

## 🚀 Key Features

-   **Airflow 3 Implementation**: Built on `apache/airflow:3.2.1`.
-   **Custom SQL SDK**: A dedicated provider located in `sql-sdk/` that demonstrates how to build custom TaskFlow decorators (`@task.sql`).
-   **Dockerized Environment**: Fully containerized setup including PostgreSQL and pgAdmin.
-   **Learning Examples**: 
    -   Task Grouping (`groups.py`)
    -   Branching Logic (`branching.py`)
    -   XComs and Data Sharing (`xcom.py`)
    -   User Processing Workflows (`user_processing.py`)

## 📂 Project Structure

```text
.
├── dags/                   # Airflow DAG definitions
├── sql-sdk/                # Custom Airflow Provider (SQL SDK)
│   ├── sql_sdk/            # Provider source code
│   └── pyproject.toml      # Package configuration
├── Images/                 # Custom Docker images (Airflow 3 + SQL SDK)
├── config/                 # Configuration for services (pgAdmin, etc.)
├── docker-compose.yaml     # Orchestration for the local environment
└── requirements.txt        # Additional Python dependencies
```

## 🛠️ Getting Started

### Prerequisites
-   Docker and Docker Compose installed.
-   Python 3.10+ (for local development/linting).

### Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd airflow-course
    ```

2.  **Build and Start the Environment**:
    The Airflow image will automatically install the local `sql-sdk` during the build process.
    ```bash
    docker compose up --build
    ```

3.  **Access the Services**:
    -   **Airflow UI**: [http://localhost:8080](http://localhost:8080) (Default: `airflow`/`airflow`)
    -   **pgAdmin**: [http://localhost:5050](http://localhost:5050)

### Advanced Startup (Scaling Workers)

To scale the environment (e.g., 3 workers) and enable optional profiles like Flower:
```bash
docker compose --profile flower up -d --build --force-recreate --scale airflow-worker=3
```

## 💻 Development with VS Code

You can connect directly to the running Airflow containers to debug or explore the environment.

### Connecting to a Running Container
1.  **Install Extensions**: Ensure you have the [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) and [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extensions installed.
2.  **Attach to Scheduler**:
    -   Open the **Docker** tab in the VS Code sidebar.
    -   Expand the **Containers** section.
    -   Right-click on the `airflow-scheduler` container.
    -   Select **"Attach Visual Studio Code"**.
3.  **Terminal Access**: Alternatively, you can right-click the container and select **"Attach Shell"** to open a terminal inside the container.

## 🧪 The SQL SDK Provider

The `sql-sdk` is a custom provider that allows you to write SQL tasks using a specialized TaskFlow decorator. 

**Example usage in a DAG:**
```python
from sql_sdk.decorators.sql import sql_task

@sql_task
def my_query():
    return "SELECT * FROM users WHERE active = true"
```

## 📝 License
This project is for educational purposes as part of the Airflow 3 course.
