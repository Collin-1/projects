# Database Migrations with SQLAlchemy

This project demonstrates database migration practices using SQLAlchemy and Alembic, working with both development and production databases.

## project instructions 
(these will clarify the projects purpose)

http://syllabus.africacode.net/projects/python-specific/sqlalchemy-migrations/

## Project Overview

The project simulates real-world database management scenarios, including:
- Creating and modifying database models
- Handling database migrations
- Managing multiple database environments (development and production)
- Dealing with common database modification scenarios

## Prerequisites

- Python 3.x
- Docker
- PostgreSQL
- SQLAlchemy
- Alembic

## Setup

1. Clone the repository:
```
   git clone https://github.com/Collin-1/projects.git
   cd projects/Collin-Makwala-261-database-migrations-with-sqlalchemy-python/
```
Install dependencies:

```pip install -r requirements.txt```

Set up Docker containers for development and production databases:

`docker-compose up -d`

Project Structure
```
├── migrations/
│   ├── versions/           # Migration files
│   ├── env.py
│   └── alembic.ini
├── model.py 
├── create_learners.py
├── create_c26_learners.py
├── create_c27_learners.py
├── create_c28_learners.py
├── docker-compose.yaml
└── requirements.txt
```

### Database Model
The Learner model includes:

- First name
- Surname
- Chatname/RocketChat username
- GitHub name
- ID number
- Personal email address (unique, required)
- Cohort
### Migration Scenarios
1. Adding New Column
Demonstrates adding a required 'cohort' column and handling existing data.

2. Renaming Column
Shows the process of safely renaming 'chatname' to 'rocketchat_user'.

3. Deleting Column
Illustrates the proper way to remove the 'id_number' column.

### Usage
```
Initialize Database
alembic upgrade head
Create New Migration
alembic revision --autogenerate -m "description"
```
### Run Scripts
```
python scripts/create_learners.py
python scripts/create_c26_learners.py
python scripts/create_c27_learners.py
python scripts/create_c28_learners.py
```
### Best Practices
Always backup production database before migrations
Test migrations on development database first
Commit migrations separately from application code
Use descriptive migration messages
Never modify existing migrations that have been applied
Always review auto-generated migrations
### Common Issues and Solutions
### Migration Conflicts
Reset development database if needed
Never reset production database
Use alembic current to check migration state
Review migration history with alembic history
Data Integrity
Always ensure data consistency
Handle NULL values appropriately
Validate data before and after migrations
Testing
# Run against development database

# Verify migrations
alembic upgrade head
alembic downgrade base
