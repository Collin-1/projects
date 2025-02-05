SELECT
    'CREATE DATABASE shop'
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            pg_database
    );