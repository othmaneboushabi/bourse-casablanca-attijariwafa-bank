from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Paramètres par défaut du pipeline
default_args = {
    'owner': 'othmane',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définition du DAG
with DAG(
    'casablanca_market_daily_etl',
    default_args=default_args,
    description='Pipeline ETL quotidien pour la bourse de Casablanca',
    schedule_interval=timedelta(days=1), # S'exécute tous les jours
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['finance', 'portfolio'],
) as dag:

    # 1. Extraction vers la couche Bronze
    task_extract_bronze = BashOperator(
        task_id='extract_to_bronze',
        bash_command='echo "Exécution du script ingestion vers MinIO (Bronze)..."'
    )

    # 2. Nettoyage vers la couche Silver
    task_transform_silver = BashOperator(
        task_id='transform_to_silver',
        bash_command='echo "Exécution de 03_bronze_to_silver.py (Parquet)..."'
    )

    # 3. Chargement dans PostgreSQL (Staging)
    task_load_postgres = BashOperator(
        task_id='load_to_postgres',
        bash_command='echo "Exécution de load_to_postgres.py..."'
    )

    # 4. Modélisation avec dbt (Gold)
    task_run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='echo "Exécution de dbt run && dbt test..."'
    )

    # L'ORDRE D'EXÉCUTION (Les dépendances)
    task_extract_bronze >> task_transform_silver >> task_load_postgres >> task_run_dbt