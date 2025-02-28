# Business Logic and API Endpoints Implementation

## Table of Contents

## Description

This phase of the HBnB project involves implementing the core functionalities of the application using Python and Flask. The goal is to build the presentation and business logic layers, define essential classes, methods, and API endpoints based on the design created in the previous phase.

## Project Structure
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```
### Folder and File Descriptions

- app/: Main application folder.
- api/: API endpoints organized by version (v1/).
- models/: Business logic classes (user.py, place.py, etc.).
- services/: Implements the Facade pattern to manage interaction between layers.
- persistence/: In-memory repository for object storage and validation.
- run.py: Flask application entry point.
- config.py: Application environment and settings configuration.
- requirements.txt: List of Python packages required.
- README.md: Project overview and documentation.

## Requirements

### Installing Dependencies

List the required Python packages in requirements.txt:
```
flask
flask-restx
```
Install dependencies:
```
pip install -r requirements.txt
```

### Running the Application

Start the Flask application:
```
python run.py
```
The app should run successfully, confirming the project structure and initial setup are ready for further development.

## Business Logic Layer

### Entities

- **User**: Represents a user of the application. A user can have multiple places.
- **Place**: Represents a place to stay. A place can have multiple reviews and multiple amenities.
- **Review**: Represents a review for a place.
- **Amenity**: Represents an amenity for a place.

### Relationships

- **User → Place**: A user can have multiple places.
- **Place → Review**: A place can have multiple reviews.
- **Place ↔ Amenity**: A place can have multiple amenities and an amenity can belong to multiple places.

### Examples

#### Creating a User

```python
from app.models.user import User

user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
print(user.first_name)  # Output: John
```

#### Creating a Place

```python
from app.models.place import Place
from app.models.user import User

owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com", password="password")
place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)
print(place.title)  # Output: Cozy Apartment
```

#### Adding a REview to a Place

```python
from app.models.review import Review

review = Review(text="Great stay!", rating=5, place=place)
place.add_review(review)
print(len(place.reviews))  # Output: 1
```

#### Creating an Amenity

```python
from app.models.amenity import Amenity

amenity = Amenity(name="Wi-Fi")
print(amenity.name)  # Output: Wi-Fi
```
