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


