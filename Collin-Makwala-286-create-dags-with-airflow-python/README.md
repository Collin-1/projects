# DAGs with Airflow

## Project Overview

This project sets up an Apache Airflow environment to manage and automate workflows for handling GitHub pull requests (PRs). The DAG (Directed Acyclic Graph) created in this project performs the following tasks:

1. **Insert Data to Database**: Grab all the open pull requests from all GitHub repositories you have access to and store them in a database.
2. **Get Latest Review Timestamp**: For each pull request, get the timestamp of the latest review and store it in the database.
3. **Send Email**: Send an email to yourself showing the top 5 PRs that need attention in order of priority. If there are fewer than 5 PRs, show those.

## Prerequisites

Before you begin, ensure you have the following:

- Docker
- Docker Compose
- Python 3.7+
- Email service (e.g., Sendinblue, MailChimp)

## Setup Instructions

### 1. Clone the Repository

```
   git clone https://github.com/Collin-1/projects.git
   cd projects/Collin-Makwala-286-create-dags-with-airflow-python/
```

### 2. Set Up Environment Variables

Create a `smtp_secrets.sh` file in the root directory and add the following environment variables:

```env
export SMTP_SERVER=<your_email_service_api_key>
export SMTP_PORT=<your_email_service_port>
export SMTP_LOGIN=<your_email_service_login>
export SMTP_PASSWORD=<your_email_service_login>
export SENDER_EMAIL=<the_sender_email>
export RECEIVER_EMAIL=<the_target_email>>

AIRFLOW_IMAGE_NAME=apache/airflow:2.3.2
AIRFLOW_UID=50000
GITHUB_TOKEN=<your_github_token>
DATABASE_URL=<the_database_url>
```

### 3. Configure Docker Compose

Ensure your `docker-compose.yaml` file is correctly configured. The provided `docker-compose.yaml` sets up an Airflow cluster with CeleryExecutor, Redis, and PostgreSQL.

### 4. Initialize Airflow

Run the following command to initialize Airflow:

```
docker-compose up airflow-init
```

### 5. Start the Airflow Services

Start all the services defined in the `docker-compose.yaml` file:

```
docker-compose up
```

### 6. Access the Airflow Web Interface

Open your web browser and go to `http://localhost:8080` to access the Airflow web interface. The default username and password are both `airflow`.


### 7. Run the DAG

Trigger the DAG manually from the Airflow web interface or wait for it to run according to the schedule.

## Notes

- Be careful with your `.gitignore`. Airflow creates a few files that you should not share.
- Ensure your GitHub token and email service API key are kept secure and not shared publicly.
