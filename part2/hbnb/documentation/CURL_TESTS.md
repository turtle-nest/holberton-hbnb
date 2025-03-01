# API Endpoint Validation and Testing Report with cURL

## 1. Validation Implementation

**User Model**:

- first_name: Must be a non-empty string, max 50 characters.
- last_name: Must be a non-empty string, max 50 characters.
- email: Must be a non-empty, valid email format, and unique.
- password: Must be a string of at least 8 characters.
- is_admin: Must be a boolean.

**Place Model**: 

- name: Must be a non-empty string.
- description: Must be a string.
- city: Must be a string.
- owner_id: Must be a valid User ID.
- latitude: Must be a float between -90 and 90.
- longitude: Must be a float between -180 and 180.
- price: Must be a non-negative float.

**Review Model**:

- text: Must be a non-empty string.
- rating: Must be an integer between 1 and 5.
- user_id: Must reference a valid User.
- place_id: Must reference a valid Place.

## 2. Test Scenarios (using cURL)

### **User Endpoint Tests**

- Create a valid user:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securePass123"
}'
```
*Expected Response*: 201 OK
```bash
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

- Create an invalid user (missing fields):
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}'
```
*Expected Response*: 400 Bad Request
```bash
{
    "error": "All fields are required"
}
```

***

### **Place Endpoint Tests**

- Create a valid place:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "name": "Cozy Cabin",
    "description": "A peaceful retreat",
    "city": "Denver",
    "owner_id": "valid-user-id",
    "latitude": 39.7392,
    "longitude": -104.9903,
    "price": 120.50
}'
```
*Expected Response*: 200 OK

- Invalid place (latitude out of range):
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "name": "Cozy Cabin",
    "latitude": 100.0
}'
```
*Expected Response*: 400 Bad Request

***

### **Review Endpoint Tests**

- Create a valid review:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "Amazing place!",
    "rating": 5,
    "user_id": "valid-user-id",
    "place_id": "valid-place-id"
}'
```
*Expected Response*: 200 OK

Invalid review (missing text):
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "rating": 5,
    "user_id": "valid-user-id",
    "place_id": "valid-place-id"
}'
```
*Expected Response*: 400 Bad Request

## 3. Test Report Summary

| Endpoint      | Test Case             | Status  | Expected Result |
|---------------|----------------------|---------|-----------------|
| /users/       | Create valid user     | ✅ Passed | 200 OK          |
| /users/       | Invalid user data     | ✅ Passed | 400 Bad Request |
| /places/      | Create valid place    | ✅ Passed | 200 OK          |
| /places/      | Latitude out of range | ✅ Passed | 400 Bad Request |
| /reviews/     | Create valid review   | ✅ Passed | 200 OK          |
| /reviews/     | Missing review text   | ✅ Passed | 400 Bad Request |


Almost all tests were successfully conducted and passed as expected, ensuring robust validation and error handling across all API endpoints.