DROP TABLE IF EXISTS customers,
employees,
products,
payments,
orders;

CREATE TABLE
	customers (
		id SERIAL PRIMARY KEY NOT NULL,
		first_name VARCHAR(50) NOT NULL,
		last_name VARCHAR(50) NOT NULL,
		gender VARCHAR NOT NULL,
		address VARCHAR(200) NOT NULL,
		phone VARCHAR(20) NOT NULL,
		email VARCHAR(100) NOT NULL,
		city VARCHAR(20) NOT NULL,
		country VARCHAR(50) NOT NULL
	);

CREATE TABLE
	employees (
		id SERIAL PRIMARY KEY NOT NULL,
		first_name VARCHAR(50) NOT NULL,
		last_name VARCHAR(50) NOT NULL,
		email VARCHAR(100) NOT NULL,
		job_title VARCHAR(20) NOT NULL
	);

CREATE TABLE
	products (
		id SERIAL PRIMARY KEY NOT NULL,
		product_name VARCHAR(100) NOT NULL,
		description VARCHAR(100) NOT NULL,
		buy_price DECIMAL NOT NULL
	);

CREATE TABLE
	payments (
		id SERIAL PRIMARY KEY NOT NULL,
		customer_id INT NOT NULL,
		payment_date DATE NOT NULL,
		amount DECIMAL NOT NULL,
		FOREIGN KEY (customer_id) REFERENCES customers (id)
	);

CREATE TABLE
	orders (
		id SERIAL PRIMARY KEY NOT NULL,
		product_id INT NOT NULL,
		payment_id INT NOT NULL,
		fulfilled_by_employee_id INT NOT NULL,
		date_required DATE NOT NULL,
		date_shipped DATE,
		status VARCHAR(20) NOT NULL,
		FOREIGN KEY (product_id) REFERENCES products (id),
		FOREIGN KEY (payment_id) REFERENCES payments (id),
		FOREIGN KEY (fulfilled_by_employee_id) REFERENCES employees (id)
	);