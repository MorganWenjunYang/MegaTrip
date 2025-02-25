create database megatrip;
use megatrip;

-- Users table to store user credentials
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trips table to store trip information
CREATE TABLE trips (
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
CREATE TABLE trip_participants (
    trip_id INT,
    user_id INT,
    PRIMARY KEY (trip_id, user_id),
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);


-- Create items table with all attributes from Item class
CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    location VARCHAR(255),
    note TEXT,
    charge DECIMAL(10,2) DEFAULT 0.00,
    payer INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE,
    FOREIGN KEY (payer) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Add indexes for better query performance
CREATE INDEX idx_trip_items ON items(trip_id);
CREATE INDEX idx_item_date ON items(date);
CREATE INDEX idx_item_payer ON items(payer);

-- Insert sample user data
INSERT INTO users (username, password) VALUES
('admin', 'admin'),
('john', 'john');

-- Insert sample trip data
INSERT INTO trips (trip_id, name, destination, start_date, end_date, creator_id, created_at, status, note) VALUES
(1, 'Summer in Paris', 'Paris, France', '2025-06-01', '2025-06-07', 1, '2025-01-01', 'Active', 'Don''t forget to visit the Eiffel Tower!'),
(2, 'Tokyo Adventure', 'Tokyo, Japan', '2025-07-15', '2025-07-25', 1, '2025-01-15', 'Planned', 'Book tickets for the Ghibli Museum.'),
(3, 'New York Weekend', 'New York, USA', '2025-03-01', '2025-03-03', 2, '2025-02-01', 'Completed', 'Had a great time at Central Park.');

-- Insert sample trip participants
INSERT INTO trip_participants (trip_id, user_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 2),
(3, 1);

