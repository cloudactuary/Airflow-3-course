FROM apache/airflow:3.2.1

# mount sql-sdk folder
RUN --mount=type=bind,src=./sql-sdk,target=/opt/airflow/sql-sdk,readonly=true \
    pip install --no-cache-dir /opt/airflow/sql-sdk