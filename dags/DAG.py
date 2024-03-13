from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from modules.analysis import load_and_clean_data, calculate_annual_global_avg, save_visualization
from modules.additional_analysis import detect_outliers
from modules.summary import generate_summary_statistics 
import pandas as pd
import logging

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'earth_surface_temperature_analysis',
    default_args=default_args,
    description='Analyze Earth Surface Temperatures',
    schedule_interval='@monthly',
)

def run_analysis():
    file_path = '/opt/airflow/data/weather_data.csv'
    output_path = '/opt/airflow/output/global_avg_temps_over_time.png'
    df = load_and_clean_data(file_path)
    annual_avg_temps = calculate_annual_global_avg(df)
    save_visualization(annual_avg_temps, output_path)

run_analysis_task = PythonOperator(
    task_id='run_analysis',
    python_callable=run_analysis,
    dag=dag,
)

def run_outlier_detection():
    file_path = '/opt/airflow/data/weather_data.csv'
    df = load_and_clean_data(file_path)
    cleaned_df = detect_outliers(df, 'AverageTemperature')
    cleaned_file_path = '/opt/airflow/output/cleaned_weather_data.csv'
    cleaned_df.to_csv(cleaned_file_path, index=False)

detect_outliers_task = PythonOperator(
    task_id='detect_outliers',
    python_callable=run_outlier_detection,
    dag=dag,
)

def run_generate_summary_statistics():
    # Load the data
    file_path = '/opt/airflow/data/weather_data.csv'
    df = load_and_clean_data(file_path)
    
    generate_summary_statistics(df)

generate_summary_statistics_task = PythonOperator(
    task_id='generate_summary_statistics',
    python_callable=run_generate_summary_statistics,
    dag=dag,
)

def should_proceed_with_detailed_analysis(**kwargs):
    # Load and clean the dataset
    file_path = '/opt/airflow/data/weather_data.csv'
    df = load_and_clean_data(file_path)
    
    annual_avg_temps = calculate_annual_global_avg(df)
    
    most_recent_year_avg_temp = annual_avg_temps.iloc[-1]['AverageTemperature']
    logging.info(f"Most Recent Year's Average Temperature: {most_recent_year_avg_temp}°C")
    
    # If the most recent year's average temperature is unusually high or low,
    # proceed with detailed analysis; otherwise, check if it's within a normal range and generate summary statistics.
    if most_recent_year_avg_temp > 25:  
        return 'proceed_with_detailed_analysis'
    elif most_recent_year_avg_temp < 10:
        return 'end_workflow'
    else:
        return 'generate_summary_statistics'


branch_task = BranchPythonOperator(
    task_id='branch_task',
    python_callable=should_proceed_with_detailed_analysis,
    provide_context=True,
    dag=dag,
)

proceed_with_detailed_analysis_task = DummyOperator(
    task_id='proceed_with_detailed_analysis',
    dag=dag,
)

end_workflow_task = DummyOperator(
    task_id='end_workflow',
    dag=dag,
)

# Branching
run_analysis_task >> branch_task
branch_task >> [proceed_with_detailed_analysis_task, generate_summary_statistics_task, end_workflow_task]

# First path
proceed_with_detailed_analysis_task >> detect_outliers_task
detect_outliers_task >> end_workflow_task

# Second path
generate_summary_statistics_task >> end_workflow_task
