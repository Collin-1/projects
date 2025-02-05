# Computer Inventory API

This project is a RESTful API for managing a computer inventory. It is built with Flask and uses SQLAlchemy for database interactions. The API allows you to list, add, update, and delete computers in the inventory.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Collin-1/projects.git
   cd projects/Collin-Makwala-263-create-a-rest-api-to-interact-with-actual-database-python/

   ```
2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    pip install -e .
    ```
4. Set up the database:
    ```
    python -c "from app import create_table; create_table()"
    ```
5. Run the application:
    ```
    python app.py
    ```

## Usage example

1. ### Add a New Computer:
To add a new computer to the inventory, send a POST request to /umuzi/api/computers with the following JSON payload:

```json
{
  "hard_drive_type": "SSD",
  "processor": "Intel Core i7",
  "amount_of_ram": 16,
  "maximum_ram": 32,
  "hard_drive_space": 512,
  "form_factor": "DESKTOP"
}
```
Example using curl:

```
curl -X POST -H "Content-Type: application/json" -d '{
  "hard_drive_type": "SSD",
  "processor": "Intel Core i7",
  "amount_of_ram": 16,
  "maximum_ram": 32,
  "hard_drive_space": 512,
  "form_factor": "DESKTOP"
}' http://localhost:5000/umuzi/api/computers
```
2. ### List All Computers
To list all computers in the inventory, send a GET request to /umuzi/api/computers. You can use query parameters page and per_page to paginate the results.

Example using curl:

```
curl -X GET "http://localhost:5000/umuzi/api/computers?page=1&per_page=10"
```
3. ### Edit an Existing Computer
To edit an existing computer, send a PUT request to /umuzi/api/computers/<id> with the following JSON payload:
```
json
{
  "hard_drive_type": "HDD",
  "processor": "AMD Ryzen 5",
  "amount_of_ram": 8,
  "maximum_ram": 16,
  "hard_drive_space": 1024,
  "form_factor": "LAPTOP"
}
```
Example using curl:

```
curl -X PUT -H "Content-Type: application/json" -d '{
  "hard_drive_type": "HDD",
  "processor": "AMD Ryzen 5",
  "amount_of_ram": 8,
  "maximum_ram": 16,
  "hard_drive_space": 1024,
  "form_factor": "LAPTOP"
}' http://localhost:5000/umuzi/api/computers/1
```
4. ### Delete a Computer
To delete a computer from the inventory, send a DELETE request to /umuzi/api/computers/<id>.

Example using curl:

```
curl -X DELETE http://localhost:5000/umuzi/api/computers/1
````
## API Endpoints
5. ### List All Computers
URL:`/umuzi/api/computers`

Method: `GET`

Query Parameters:

- `page `(optional): The page number (default: 1)

- `per_page` (optional): The number of items per page (default: 10)

Response: `200 OK` with a list of computers

6. ### Add a New Computer
URL: /umuzi/api/computers

Method: POST

Request Body:

    ```json
    {
    "hard_drive_type": "SSD or HDD",
    "processor": "Processor name",
    "amount_of_ram": RAM amount in GB,
    "maximum_ram": Maximum RAM in GB,
    "hard_drive_space": Hard drive space in GB,
    "form_factor": "DESKTOP or LAPTOP"
    }```
Response: `201 Created` with the created computer

7. ### Edit an Existing Computer
URL: `/umuzi/api/computers/<int:id>`

Method:`PUT`

Request Body:

```json
{
  "hard_drive_type": "SSD or HDD",
  "processor": "Processor name",
  "amount_of_ram": RAM amount in GB,
  "maximum_ram": Maximum RAM in GB,
  "hard_drive_space": Hard drive space in GB,
  "form_factor": "DESKTOP or LAPTOP"
}
```
Response: `200 OK` with a success message

8. ### Delete a Computer
URL: `/umuzi/api/computers/<int:id>`

Method: `DELETE`

Response: `200 OK` with a success message

## Data Models

### Computer

-`id` (integer, primary key)

- `hard_drive_type` (enum: SSD or HDD, not nullable)

- `processor` (string, not nullable)

- `amount_of_ram` (integer, not nullable)

- `maximum_ram` (integer, not nullable)

- `hard_drive_space` (integer, not nullable)

- `form_factor` (enum: DESKTOP or LAPTOP, not nullable)

### Enumerations
####HardDriveType
- `SSD`

- `HDD`

### FormFactor
- `DESKTOP`

- `LAPTOP`
