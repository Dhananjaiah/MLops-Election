"""
Airflow DAG for election model training pipeline.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Default arguments
default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'email': ['mlops@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'election_training_pipeline',
    default_args=default_args,
    description='End-to-end training pipeline for election prediction model',
    schedule_interval='0 2 * * 0',  # Weekly on Sunday at 2 AM
    start_date=days_ago(1),
    catchup=False,
    tags=['ml', 'training', 'election'],
)


def generate_dataset():
    """Generate or fetch latest election dataset."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from src.data.make_dataset import main as make_dataset_main
    make_dataset_main()


def preprocess_data():
    """Preprocess election data."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from src.data.preprocess import main as preprocess_main
    preprocess_main()


def engineer_features():
    """Engineer features from preprocessed data."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from src.data.features import main as features_main
    features_main()


def train_models():
    """Train multiple models and select best one."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from src.train.train import main as train_main
    train_main()


def evaluate_model():
    """Evaluate trained model."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from src.train.evaluate import main as evaluate_main
    evaluate_main()


def compare_models():
    """Compare model performance."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from src.train.compare_models import main as compare_main
    compare_main()


def register_model():
    """Register model in MLflow registry."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    import mlflow
    from src.utils.config import Config
    
    mlflow.set_tracking_uri(Config.MLFLOW_TRACKING_URI)
    
    # Get latest run
    experiment = mlflow.get_experiment_by_name(Config.MLFLOW_EXPERIMENT_NAME)
    if experiment:
        runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time DESC"], max_results=1)
        if not runs.empty:
            run_id = runs.iloc[0]['run_id']
            
            # Register model
            model_uri = f"runs:/{run_id}/model"
            mlflow.register_model(model_uri, Config.MLFLOW_MODEL_REGISTRY_NAME)
            
            print(f"Model registered: {model_uri}")


# Define tasks
task_generate = PythonOperator(
    task_id='generate_dataset',
    python_callable=generate_dataset,
    dag=dag,
)

task_preprocess = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

task_features = PythonOperator(
    task_id='engineer_features',
    python_callable=engineer_features,
    dag=dag,
)

task_train = PythonOperator(
    task_id='train_models',
    python_callable=train_models,
    dag=dag,
)

task_evaluate = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    dag=dag,
)

task_compare = PythonOperator(
    task_id='compare_models',
    python_callable=compare_models,
    dag=dag,
)

task_register = PythonOperator(
    task_id='register_model',
    python_callable=register_model,
    dag=dag,
)

# DVC version control (optional)
task_dvc_push = BashOperator(
    task_id='dvc_push',
    bash_command='cd /opt/airflow/dags/repo && dvc push || echo "DVC not configured"',
    dag=dag,
)

# Notification task
task_notify = BashOperator(
    task_id='send_notification',
    bash_command='echo "Training pipeline completed successfully!" | mail -s "ML Pipeline Success" mlops@example.com || echo "Mail not configured"',
    dag=dag,
)

# Define task dependencies
task_generate >> task_preprocess >> task_features >> task_train >> task_evaluate >> task_compare >> task_register >> task_dvc_push >> task_notify
