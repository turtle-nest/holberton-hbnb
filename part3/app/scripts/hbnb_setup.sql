-- Drop existing tables if they exist to ensure a clean setup
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS place;
DROP TABLE IF EXISTS amenity;
DROP TABLE IF EXISTS users;

-- Create the 'users' table to store user information
CREATE TABLE Users (
    id CHAR(36) PRIMARY KEY, 
    first_name VARCHAR(255) NOT NULL, 
    last_name VARCHAR(255) NOT NULL, 
    email VARCHAR(255) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create the 'place' table to store places available for booking
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY, 
    title VARCHAR(255) NOT NULL, 
    description TEXT, 
    price DECIMAL(10,2) NOT NULL, 
    latitude FLOAT, 
    longitude FLOAT, 
    owner_id CHAR(36) NOT NULL, 
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create the 'review' table to store user reviews for places
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY, 
    text TEXT NOT NULL, 
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL, 
    user_id CHAR(36) NOT NULL, 
    place_id CHAR(36) NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE,
    CONSTRAINT unique_user_place_review UNIQUE (user_id, place_id)
);

-- Create the 'amenity' table to store available amenities
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY, 
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Create the 'place_amenity' table to establish a many-to-many relationship between places and amenities
CREATE TABLE Place_amenity (
    place_id CHAR(36) NOT NULL, 
    amenity_id CHAR(36) NOT NULL, 
    PRIMARY KEY (place_id, amenity_id), 
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenity(id) ON DELETE CASCADE
);

-- Insert an admin user with a predefined UUID
INSERT INTO users (id, first_name, last_name, email, password, is_admin) 
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 
    'Admin', 
    'HBnB', 
    'admin@hbnb.io', 
    '$2b$12$y6wM5KtUXxHF/N8T7xLoqOfjOCp6cFJ8HzJ9O2gjJpNqF6R76Q6p2', 
    TRUE
);

-- Insert initial amenities with randomly generated UUIDs
INSERT INTO amenity (id, name) VALUES
    (UUID(), 'WiFi'),
    (UUID(), 'Swimming Pool'),
    (UUID(), 'Air Conditioning');

-- Retrieve all users to verify insertion
SELECT * FROM users;

-- Retrieve all amenities to verify insertion
SELECT * FROM amenity;

-- Insert a new standard user with a generated UUID
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (UUID(), 'John', 'Doe', 'john@example.com', '$2b$12$y6wM5KtUXxHF/N8T7xLoqOfjOCp6cFJ8HzJ9O2gjJpNqF6R76Q6p2', FALSE);

-- Retrieve all users to verify the new user was added
SELECT * FROM users;
