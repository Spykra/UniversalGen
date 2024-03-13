FROM apache/airflow:2.8.2

WORKDIR /opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./dags ./dags
COPY ./data ./data
COPY ./modules ./dags/modules 

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/dags:/opt/airflow/dags/modules"
