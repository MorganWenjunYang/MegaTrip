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


INSERT INTO items (trip_id, name, description, date, location, note, charge, start_time, end_time, payer) VALUES
(1, 'Visit Eiffel Tower', 'Iconic landmark visit with guided tour', '2024-07-15', 'Paris, France', 'Book evening tour for best views', 25.50, '18:30:00', '20:30:00', 'Alice'),
(1, 'Louvre Museum', 'Art museum tour', '2024-07-16', 'Paris, France', 'Get skip-the-line tickets', 17.00, '10:00:00', '14:00:00', 'Bob'),
(1, 'Seine River Cruise', 'Evening dinner cruise', '2024-07-16', 'Seine River, Paris', 'Vegetarian meal requested', 89.00, '19:00:00', '22:00:00', 'Charlie'),
(2, 'Mount Fuji Tour', 'Day trip to Mount Fuji', '2024-08-01', 'Mount Fuji, Japan', 'Weather dependent', 120.00, '08:00:00', '17:00:00', 'David'),
(2, 'Sushi Making Class', 'Traditional sushi workshop', '2024-08-02', 'Tokyo, Japan', 'Ingredients included', 75.00, '11:00:00', '13:30:00', 'Eve');