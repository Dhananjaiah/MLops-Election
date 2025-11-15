"""
Airflow DAG for batch scoring pipeline.
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
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

# DAG definition
dag = DAG(
    'election_batch_scoring',
    default_args=default_args,
    description='Daily batch prediction for election outcomes',
    schedule_interval='0 3 * * *',  # Daily at 3 AM
    start_date=days_ago(1),
    catchup=False,
    tags=['ml', 'batch', 'prediction', 'election'],
)


def fetch_new_data():
    """Fetch new election data for prediction."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from pathlib import Path
    from src.data.make_dataset import generate_synthetic_election_data, save_dataset
    from src.utils.config import Config
    from datetime import datetime
    
    # In production, this would fetch real data from a database or API
    # For demo, we generate synthetic data
    
    timestamp = datetime.now().strftime('%Y%m%d')
    output_path = Config.DATA_DIR / "incoming" / f"election_data_{timestamp}.csv"
    
    df = generate_synthetic_election_data(n_samples=500, random_state=int(timestamp))
    save_dataset(df, output_path)
    
    print(f"New data fetched: {output_path}")
    return str(output_path)


def preprocess_new_data(**context):
    """Preprocess new data for prediction."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from pathlib import Path
    import pandas as pd
    from src.data.preprocess import ElectionDataPreprocessor
    from src.utils.config import Config
    
    # Get input path from previous task
    input_path = context['ti'].xcom_pull(task_ids='fetch_new_data')
    
    # Load data
    df = pd.read_csv(input_path)
    
    # Preprocess
    preprocessor = ElectionDataPreprocessor()
    scaler_path = Config.MODELS_DIR / "scaler.pkl"
    if scaler_path.exists():
        preprocessor.load_scaler(scaler_path)
    
    df_processed = preprocessor.preprocess(df, fit_scaler=False)
    
    # Save processed data
    output_path = Path(input_path).parent / f"processed_{Path(input_path).name}"
    df_processed.to_csv(output_path, index=False)
    
    print(f"Data preprocessed: {output_path}")
    return str(output_path)


def run_batch_predictions(**context):
    """Run batch predictions on new data."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    from pathlib import Path
    from src.serving.batch_predict import BatchPredictor
    from datetime import datetime
    
    # Get input path from previous task
    input_path = context['ti'].xcom_pull(task_ids='preprocess_new_data')
    
    # Define output path
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = Path('/opt/airflow/dags/repo/predictions') / f"predictions_{timestamp}.csv"
    
    # Run predictions
    predictor = BatchPredictor()
    predictor.predict_from_file(Path(input_path), output_path)
    
    print(f"Predictions saved: {output_path}")
    return str(output_path)


def store_predictions(**context):
    """Store predictions in database or data warehouse."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    import pandas as pd
    
    # Get predictions path from previous task
    predictions_path = context['ti'].xcom_pull(task_ids='run_batch_predictions')
    
    # Load predictions
    df_predictions = pd.read_csv(predictions_path)
    
    # In production, this would store in a database
    # For demo, we just log some statistics
    
    print(f"Storing {len(df_predictions)} predictions")
    print(f"Prediction distribution:\n{df_predictions['predicted_winner'].value_counts()}")
    print(f"Average confidence: {df_predictions['confidence'].mean():.4f}")
    
    # Simulate database storage
    print("Predictions stored in database (simulated)")


def generate_report(**context):
    """Generate daily prediction report."""
    import sys
    sys.path.insert(0, '/opt/airflow/dags/repo')
    
    import pandas as pd
    import json
    from pathlib import Path
    from datetime import datetime
    
    # Get predictions path
    predictions_path = context['ti'].xcom_pull(task_ids='run_batch_predictions')
    
    # Load predictions
    df_predictions = pd.read_csv(predictions_path)
    
    # Generate report
    report = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "total_predictions": len(df_predictions),
        "prediction_distribution": df_predictions['predicted_winner'].value_counts().to_dict(),
        "average_confidence": float(df_predictions['confidence'].mean()),
        "min_confidence": float(df_predictions['confidence'].min()),
        "max_confidence": float(df_predictions['confidence'].max()),
        "predictions_file": predictions_path
    }
    
    # Save report
    report_path = Path('/opt/airflow/dags/repo/reports') / f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report generated: {report_path}")


# Define tasks
task_fetch = PythonOperator(
    task_id='fetch_new_data',
    python_callable=fetch_new_data,
    dag=dag,
)

task_preprocess = PythonOperator(
    task_id='preprocess_new_data',
    python_callable=preprocess_new_data,
    provide_context=True,
    dag=dag,
)

task_predict = PythonOperator(
    task_id='run_batch_predictions',
    python_callable=run_batch_predictions,
    provide_context=True,
    dag=dag,
)

task_store = PythonOperator(
    task_id='store_predictions',
    python_callable=store_predictions,
    provide_context=True,
    dag=dag,
)

task_report = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    provide_context=True,
    dag=dag,
)

task_notify = BashOperator(
    task_id='send_notification',
    bash_command='echo "Batch scoring completed!" | mail -s "Batch Scoring Complete" mlops@example.com || echo "Mail not configured"',
    dag=dag,
)

# Define task dependencies
task_fetch >> task_preprocess >> task_predict >> task_store >> task_report >> task_notify
