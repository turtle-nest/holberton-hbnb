# Swagger Documentation

## 1. Introduction

- Goal: Test the various API endpoints to ensure behavior conforms to specifications.

- Test environment: Specify the URL of the test API (e.g. http://127.0.0.1:5000/api/v1/).

- Noticed: 500 errors are related to a missing database. A 500 (Internal Server Error) error usually indicates that there is a server-side problem, often caused by a lack of data management or an attempt to access a resource that does not exist (such as an unconfigured database)

***

## 2. User Creation and Recovery Testing

### Scenario 1: Creating a user with an existing email

- Method: POST
- URL: /users
-Request:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "password123"
}
```
- Expected status code: 400 Bad Request
- Description: The API should return a 400 error if the email already exists.

### Scenario 2: Recovery of a non-existent user

- Method: GET
- URL: /users/<nonexistent_id>
- Expected status code: 404 Not Found
- Description: The API should return 404 if the user does not exist.

***

## 3. User and Device Update Tests

### Scenario 3: Updating a user with invalid data

- Method: PUT
- URL: /users/<user_id>
- Request:
```json
{
"email": "invalid_email"
}
```
- Expected status code: 400 Bad Request
- Description: The API should return 400 if the data is invalid (e.g. incorrect email format).

***

## 4. Equipment Testing

### Scenario 4: Sending JSON data to create an equipment

- Method: POST
- URL: /amenities
- Request:
```json
{
  "name": "New equipement"
}
```
- Expected status code: 201 Created
- Description: The API should return 201 if the equipment creation is successful.

### Scenario 5: Retrieving equipment

- Method: GET
- URL: /amenities
- Expected status code: 200 OK
- Description: The API should return the list of existing equipment.

### Scenario 6: Updating an existing equipment

- Method: PUT
- URL: /amenities/<amenities_id>
- Request:
```json
{
"name": "Updated Equipment"
}
```
- Expected status code: 200 OK
- Description: The API should return 200 if the equipment is updated successfully.

***

## 5. Review Testing

### Scenario 7: Creating a review

- Method: POST
- URL: /api/v1/reviews/
- Request:
```json
{
"text": "Excellent place!",
"rating": 5,
"user_id": "123",
"place_id": "456",
}
```
- Expected status code: 201 Created
- Description: The API should return 201 if the review is successfully created.

### Scenario 8: Retrieving reviews

- Method: GET
- URL: /api/v1/reviews/ or /api/v1/places/<place_id>/reviews
- Expected status code: 200 OK
- Description: The API should return existing reviews.

### Scenario 9: Editing a review

- Method: PUT
- URL: /api/v1/reviews/<review_id>
- Request:
```json
{
"review": "Updated review content",
"rating": 4
}
```
- Expected status code: 200 OK
- Description: The API should return 200 if the review is edited.

### Scenario 10: Deleting a review

- Method: DELETE
- URL: /api/v1/reviews/<review_id>
- Expected status code: 200 OK
- Description: The API should return 200 if the review is deleted.

## 6. Conclusion

This document outlines the test scenarios for various API endpoints of the project, including user creation and recovery, equipment management, and review operations. By executing these tests with Swagger, we ensure that the API behaves as expected and returns the correct HTTP status codes for different situations.
