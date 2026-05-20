wget https://airflow.apache.org/docs/apache-airflow/3.2.1/docker-compose.yaml

mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=50000" > .env

sed -i "s/AIRFLOW__CORE__LOAD_EXAMPLES: 'true'/AIRFLOW__CORE__LOAD_EXAMPLES: 'false'/" ./docker-compose.yaml
echo "AIRFLOW_FERNET_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")" >> .env
sed -i 's/${FERNET_KEY}/${AIRFLOW_FERNET_KEY}/' ./docker-compose.yaml

docker compose -p airflow_course up -d --build --force-recreate

# docker compose -p airflow_course down -v --remove-orphans
