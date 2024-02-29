-- Drop the database if it exists
DROP DATABASE IF EXISTS your_database;

-- Create the database
CREATE DATABASE your_database;

-- Use the newly created database
USE your_database;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password CHAR(64) NOT NULL
);

-- Insert a sample user
INSERT INTO users (name, email, password) VALUES ('John Doe', 'john.doe@example.com', '12345');
