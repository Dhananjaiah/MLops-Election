"""
Airflow DAG for automated retraining on drift detection.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

# Default arguments
default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'email': ['mlops@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'election_retrain_on_drift',
    default_args=default_args,
    description='Automated model retraining triggered by drift detection',
    schedule_interval='0 */6 * * *',  # Every 6 hours
    start_date=days_ago(1),
    catchup=False,
    tags=['ml', 'drift', 'retrain', 'election'],
)


def collect_recent_data():
    """Collect recent production data."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from pathlib import Path
    from src.data.make_dataset import generate_synthetic_election_data, save_dataset
    from src.utils.config import Config
    from datetime import datetime
    
    # In production, collect recent data from production database
    # For demo, generate synthetic data
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = Config.DATA_DIR / "production" / f"recent_data_{timestamp}.csv"
    
    df = generate_synthetic_election_data(n_samples=1000, random_state=int(timestamp[:8]))
    save_dataset(df, output_path)
    
    print(f"Recent data collected: {output_path}")
    return str(output_path)


def detect_drift(**context):
    """Detect drift in recent data."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    import pandas as pd
    from pathlib import Path
    from src.monitoring.drift_monitoring import DriftMonitor
    from src.data.features import ElectionFeatureEngineering
    from src.utils.config import Config
    
    # Get recent data path
    recent_data_path = context['ti'].xcom_pull(task_ids='collect_recent_data')
    
    # Load reference data
    reference_path = Config.DATA_DIR / "features" / "train_features.csv"
    if not reference_path.exists():
        print("Reference data not found. Skipping drift detection.")
        return False
    
    reference_data = pd.read_csv(reference_path)
    
    # Load and process recent data
    recent_data = pd.read_csv(recent_data_path)
    
    # Engineer features for recent data
    from src.data.preprocess import ElectionDataPreprocessor
    preprocessor = ElectionDataPreprocessor()
    scaler_path = Config.MODELS_DIR / "scaler.pkl"
    if scaler_path.exists():
        preprocessor.load_scaler(scaler_path)
    
    recent_data_processed = preprocessor.preprocess(recent_data, fit_scaler=False)
    
    feature_engineer = ElectionFeatureEngineering()
    recent_data_features = feature_engineer.engineer_features(recent_data_processed)
    
    # Get feature names
    feature_names = feature_engineer.get_all_feature_names()
    
    # Detect drift
    monitor = DriftMonitor()
    drift_report = monitor.detect_data_drift(
        reference_data,
        recent_data_features,
        feature_names
    )
    
    # Save drift report
    report_path = Config.BASE_DIR / "reports" / "drift" / f"drift_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    monitor.save_drift_report(report_path)
    
    drift_detected = drift_report['drift_detected']
    print(f"Drift detected: {drift_detected}")
    
    # Store drift status in XCom
    context['ti'].xcom_push(key='drift_detected', value=drift_detected)
    context['ti'].xcom_push(key='drift_share', value=drift_report['drift_share'])
    
    return drift_detected


def check_drift_decision(**context):
    """Branch based on drift detection."""
    drift_detected = context['ti'].xcom_pull(task_ids='detect_drift', key='drift_detected')
    
    if drift_detected:
        print("Drift detected. Triggering retrain pipeline.")
        return 'trigger_retrain'
    else:
        print("No drift detected. Skipping retrain.")
        return 'skip_retrain'


def trigger_retrain():
    """Trigger the training pipeline."""
    from airflow.api.common.trigger_dag import trigger_dag
    
    try:
        trigger_dag(
            dag_id='election_training_pipeline',
            run_id=f'drift_triggered_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            conf={'triggered_by': 'drift_detection'}
        )
        print("Training pipeline triggered successfully!")
    except Exception as e:
        print(f"Failed to trigger training pipeline: {e}")
        print("Manually trigger the training pipeline.")


def evaluate_new_model():
    """Evaluate the newly trained model."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from src.train.evaluate import main as evaluate_main
    
    print("Evaluating newly trained model...")
    evaluate_main()


def deploy_to_staging():
    """Deploy new model to staging environment."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    import shutil
    from pathlib import Path
    from src.utils.config import Config
    
    # Copy model to staging directory
    source_model = Config.MODELS_DIR / "best_model.pkl"
    staging_dir = Path('/opt/staging/models')
    staging_dir.mkdir(parents=True, exist_ok=True)
    
    staging_model = staging_dir / f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
    shutil.copy(source_model, staging_model)
    
    print(f"Model deployed to staging: {staging_model}")


def send_drift_alert(**context):
    """Send alert when drift is detected."""
    drift_share = context['ti'].xcom_pull(task_ids='detect_drift', key='drift_share')
    
    message = f"""
    ⚠️ DRIFT ALERT ⚠️
    
    Data drift has been detected in the election prediction model.
    Drift Share: {drift_share:.2%}
    
    Automated retraining has been triggered.
    
    Timestamp: {datetime.now().isoformat()}
    """
    
    print(message)
    # In production, send via email, Slack, PagerDuty, etc.


# Define tasks
task_collect = PythonOperator(
    task_id='collect_recent_data',
    python_callable=collect_recent_data,
    dag=dag,
)

task_drift = PythonOperator(
    task_id='detect_drift',
    python_callable=detect_drift,
    provide_context=True,
    dag=dag,
)

task_branch = BranchPythonOperator(
    task_id='check_drift_decision',
    python_callable=check_drift_decision,
    provide_context=True,
    dag=dag,
)

task_retrain = PythonOperator(
    task_id='trigger_retrain',
    python_callable=trigger_retrain,
    dag=dag,
)

task_evaluate = PythonOperator(
    task_id='evaluate_new_model',
    python_callable=evaluate_new_model,
    dag=dag,
)

task_deploy = PythonOperator(
    task_id='deploy_to_staging',
    python_callable=deploy_to_staging,
    dag=dag,
)

task_alert = PythonOperator(
    task_id='send_drift_alert',
    python_callable=send_drift_alert,
    provide_context=True,
    dag=dag,
)

task_skip = DummyOperator(
    task_id='skip_retrain',
    dag=dag,
)

task_end = DummyOperator(
    task_id='end',
    trigger_rule='none_failed_min_one_success',
    dag=dag,
)

# Define task dependencies
task_collect >> task_drift >> task_branch
task_branch >> task_retrain >> task_evaluate >> task_deploy >> task_alert >> task_end
task_branch >> task_skip >> task_end
