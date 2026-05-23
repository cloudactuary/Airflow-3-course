

### Start containers

```sh
docker compose --profile flower up -d --build --force-recreate --scale airflow-worker=3
```
and connect to running container `airflow-scheduler`.
