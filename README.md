# Earth Surface Temperature Analysis Project

This project analyzes earth surface temperature data, leveraging Apache Airflow to orchestrate the workflow, Docker for environment management, and PostgreSQL and Redis as supporting services. The analysis includes data cleaning, calculation of global average temperatures, outlier detection, and summarization of the findings.

## Installation

Clone this repository to your local machine. Ensure you have Docker installed.

```bash
git clone <repository-url>
cd <repository-name>
```

## Docker Compose
The docker-compose.yml file defines the services needed for the project: PostgreSQL, Redis, Airflow Webserver, Airflow Scheduler, and Airflow Init. It ensures all components are properly linked and configured.

To start the project, run:

```bash
docker-compose up -d
```

This command will build and start all the required services defined in docker-compose.yml. The Airflow web interface will be available at http://localhost:8080.

## Components
### DAG Definition: Defines the workflow and tasks for analyzing earth surface temperature data.
### Modules:
- analysis.py: Contains functions for loading, cleaning, and analyzing temperature data.
- additional_analysis.py: Functions for additional data analysis, like outlier detection.
- summary.py: Generates summary statistics from the cleaned data.
- post_analysis.py: Generates a summary report from the analysis results.