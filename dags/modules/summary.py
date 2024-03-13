import pandas as pd

def generate_summary_statistics(df):
    summary = df.describe()
    summary.to_csv('/opt/airflow/output/summary_statistics.csv')
    print("Summary statistics generated.")
