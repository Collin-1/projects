-- 7. SELECT ALL records from table Customers.
SELECT
  *
FROM
  customers;

-- 8. SELECT records only from the name column in the Customers table.
SELECT
  first_name,
  last_name
FROM
  customers;

-- 9. Show the full name of the Customer whose CustomerID is 1.
SELECT
  first_name,
  last_name
FROM
  customers
WHERE
  ID = 1;

-- 10. UPDATE the record for CustomerID = 1 on the Customer table so that the name is “Lerato Mabitso”.
UPDATE customers
SET
  first_name = 'Lerato',
  last_name = 'Mabitso'
WHERE
  id = 1;

-- 11. DELETE the record from the Customers table for customer 2 (CustomerID = 2).
DELETE FROM customers
WHERE
  id = 2;

-- 12. Select all unique statuses from the Orders table and get a count of the number of orders for each unique status.
SELECT
  status,
  COUNT(*)
FROM
  orders
GROUP BY
  status;

-- 13. Return the MAXIMUM payment made on the PAYMENTS table.
SELECT
  MAX(amount)
FROM
  payments;

-- 14. Select all customers from the “Customers” table, sorted by the “Country” column.
SELECT
  *
FROM
  customers
ORDER BY
  country;

-- 15. Select all products with a price BETWEEN R100 and R600.
SELECT
  *
FROM
  products
WHERE
  buy_price BETWEEN 100 AND 600;

-- 16. Select all fields from “Customers” where the country is “Germany” AND the city is “Berlin”.
SELECT
  *
FROM
  customers
WHERE
  country = 'Germany'
  AND city = 'Berlin';

-- 17. Select all fields from “Customers” where the city is “Cape Town” OR “Durban”.
SELECT
  *
FROM
  customers
WHERE
  city = 'Durban'
  OR city = 'Cape Town';

-- 18. Select all records from Products where the Price is GREATER than R500
SELECT
  *
FROM
  products
WHERE
  buy_price > 500;

-- 19. Return the sum of the Amounts on the Payments table.
SELECT
  SUM(amount)
FROM
  payments;

-- 20. Count the number of shipped orders in the Orders table.
SELECT
  COUNT(*)
FROM
  orders
WHERE
  status = 'Shipped';

-- 21. Return the average price of all Products, in Rands and Dollars (assume the exchange rate is R12 to the Dollar).
SELECT
  'R ' || ROUND(AVG(buy_price), 2) AS avg_rand,
  '$ ' || ROUND(AVG(buy_price) / 12, 2) AS avg_dollar
FROM
  Products;

-- 22. Using INNER JOIN create a query that selects all Payments with Customer information.
SELECT
  *
FROM
  payments AS p
  INNER JOIN customers AS c on p.customer_id = c.id;

-- 23. Select all products that have turnable front wheels.
SELECT
  *
FROM
  products
WHERE
  description ILIKE 'Turnable%';