# Shop Database

## NB
If you can not access adminer with the instructed prompts, delete the old volume by following the instructions below:
1. Make sure that the volumes are not in use by running `docker-compose down` in your terminal
2. Get the list of volumes by running running `docker volume ls` 
3. Delete a volume connected to the adminer, it should be similar to `collin-makwala-200-sql-_postgres_data`, by running `docker volume rm collin-makwala-200-sql-_postgres_data`
4. Now that you have deleted the volume start up the process from step number 2, 'Running the docker compose file'.

# Set up

1. Cloning the Repository:

Cloning the repository pulls down a full copy of all the repository data associated with the GitHub.com uploads
Use the following command in Windows Terminal or Command Prompt to clone the repository:
```
   git clone https://github.com/Collin-1/projects.git
   cd projects/Collin-Makwala-186-consume-github-api-python/
```

2. Running the docker-compose file:

The docker Compose file sets up a Postgres database and an Adminer interface for managing the database, both of which can be accessed from the host machine. 
Navigate to the directory containing the docker-compose file using the command below.
```
cd Collin-Makwala-200-sql-/
```
To start the services run the following command in your terminal, 
```
docker-compose up
```
This will create the database and run the .sql files in the ./src folder

3. View the database

To view the database, use this link http://localhost:8080/ to access adminer and enter the following login details:
```
system = PostgreSQL
server = postgres
username = user
password = pass
database = shop
```

Once logged in adminer, explore the database:
- Navigate through the database to examine the tables and data structure.
- Review the relationships between tables by examining the foreign key constraints.

# The **shop** database

Below is the shop database and its tables.


## customers table


|id|first_name|last_name|gender|address|phone|email|city|country|
|---|---------|---------|------|-------|-----|-----|----|-------|
|3|Leon|Glen|Male|"81 Everton Rd, Gillits"|"0820832830"|Leon@gmail.com|Durban|South Africa|
|4|Charl|Muller|Male|290A Dorset Ecke|+44856872553|Charl.muller@yahoo.com|Berlin|Germany|
|5|Julia|Stein|Female|2 Wernerring|+448672445058|Js234@yahoo.com|Frankfurt|Germany|
|1|Lerato|Mabitso|Male|284 chaucer st|"084789657"|john@gmail.com|Johannesburg|South Africa|

The customers table is referenced by the payments table through customer_id


## employees table

|id|first_name|last_name|email|job_title|
|---|--------|---------|-----|---------|
|1|Kani|Matthew|mat@gmail.com|Manager|
|2|Lesly|Cronje|LesC@gmail.com|Clerk|
|3|Gideon|Maduku|m@gmail.com|Accountant|

The employees table is referenced by the orders table through the fulfilled_by_employee_id


## orders table

|id|product_id|payment_id|fulfilled_by_employee_id|date_required|date_shipped|status|
|---|---|---|---|---|---|---|
|1|1|1|2|2018-05-09||Not shipped|
|2|1|2|2|2018-04-09|2018-03-09|Shipped|
|3|3|3|3|2018-06-09||Not shipped|

The product_id links to the products table

The payment_id links to the payments table

The fulfilled_by_employee_id links to the employees table


## payments table

|id|customer_id|payment_date|amount|
|---|---|---|---|
|1|1|2018-01-09|150.75|
|2|5|2018-03-09|150.75|
|3|4|2018-03-09|"700.60"|

The cusomter_id is linked to the id in the customers tables

The payments table is referenced by the orders table through the payment_id


## products table

|id|product_name|description|buy_price|
|---|---|---|---|
|1|Harley Davidson Chopper|"This replica features a working kickstand, front suspension, gear-shift lever"|150.75|
|2|Classic Car|"Turnable front wheels steering function"|550.75|
|3|Sportscar|"Turnable front wheels steering function"|700.60|

The products table is referenced by the orders table through the products_id