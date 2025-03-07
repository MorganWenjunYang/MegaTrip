-- Add this at the top of your file
SELECT 'INIT SCRIPT IS RUNNING' as message;

-- Check if database exists, if not create it
CREATE DATABASE IF NOT EXISTS megatrip;
USE megatrip;

-- Users table to store user credentials
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trips table to store trip information
CREATE TABLE IF NOT EXISTS trips (
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    creator_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Active', 'Planned', 'Completed') DEFAULT 'Planned',
    note TEXT,
    FOREIGN KEY (creator_id) REFERENCES users(user_id)
);

-- Trip participants junction table for many-to-many relationship
CREATE TABLE IF NOT EXISTS trip_participants (
    trip_id INT,
    user_id INT,
    PRIMARY KEY (trip_id, user_id),
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);


-- Create items table with all attributes from Item class
CREATE TABLE IF NOT EXISTS items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    trip_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    date DATE,
    location VARCHAR(255),
    note TEXT,
    charge DECIMAL(10,2) DEFAULT 0.00,
    start_time TIME,
    end_time TIME,
    payer VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE,
    INDEX idx_trip_id (trip_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
