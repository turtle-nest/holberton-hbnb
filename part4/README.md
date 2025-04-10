# HBNB - Simple Web Client (Part 4)

This is Part 4 of the HBNB web project, which focuses on building a dynamic and interactive web page to display detailed information about a specific place. The frontend is connected to a Flask RESTful API that provides data about places, amenities, reviews, and users.

## 🌟 Objectives

- Develop a user-friendly interface following design specifications.
- Implement client-side functionality to interact with the back-end API.
- Handle secure and efficient data manipulation using JavaScript.
- Apply modern front-end practices to build a dynamic single-page experience.

## 🎯 Learning Goals

- Apply HTML5, CSS3, and modern JavaScript (ES6) in a full-stack project.
- Interact with REST APIs using the Fetch API (AJAX).
- Manage authentication via JWT and handle user sessions with cookies.
- Enhance UX by manipulating the DOM without page reloads.

## 🛠️ Technologies

- HTML5 + CSS3 (Basic styling)
- JavaScript (ES6+)
- Fetch API for HTTP requests
- Flask (Backend API)
- SQLAlchemy (ORM for data)
- JWT (for user authentication)

## 🔄 How It Works

1. The user visits `place.html?place_id=<id>`.
2. JavaScript fetches place details from `/api/v1/places/<id>`.
3. Amenities and reviews are loaded and injected into the DOM.
4. If the user is logged in (JWT in cookie), the review form is shown.
5. Submitting the form sends a `POST` request to create a new review.

## 🧰 Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── v1/places.py, reviews.py, ...
│   │   ├── views.py
│   ├── models/
│   ├── static/
│   │   ├── styles.css
│   │   ├── script.js
│   │   └── images/
│   ├── templates/
│   │   ├── index.html, login.html, place.html, add_review.html
│   └── extensions.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
```
---

## 🚀 Setup & Run Instructions

### 1. Clone the repository

```bash
git clone https://github.com/turtle-nest/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4
```

### 2. Create a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
- flask
- flask-restx
- flask-bcrypt
- flask-jwt-extended
- sqlalchemy
- flask-sqlalchemy
- flask-cors
- sqlite-web

```bash
pip install -r requirements.txt
```

### 4. Run the Flask app

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

By default, the app will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ⚠️ CORS

If your frontend is served on a different origin (e.g. `file://`, or `localhost:5500` with Live Server), enable CORS in Flask:

```python
# in app/__init__.py or run.py
from flask_cors import CORS
CORS(app)
```

---

### ❓ Why CORS is Important

If you open your frontend using a different origin (like `file://` or Live Server on `localhost:5500`), and try to fetch data from your Flask backend (e.g., `localhost:5000`), the browser will block the request for security reasons. This is known as a **CORS error**.

To fix it, you must enable CORS support in your Flask backend using `flask_cors`:

This will ensure your frontend can communicate properly with the API when running on separate origins during development.

---
Parfait ! Voici la **section corrigée** à intégrer dans ton `README.md`, en précisant que le fichier s'appelle `development.db` et que la vérification se fait avec **sqlite-web** :

---

### 🗃️ Initialize the Database

To create your tables and insert sample data (users, places, reviews, amenities), you must run the script `init_db.py`.

> Make sure your virtual environment is activated and all dependencies are installed before running this step.

#### 1. Check your database configuration

The database URI is usually defined in `config.py`. Example:

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"
```

You can change this path if needed.

#### 2. Run the database initialization script

```bash
python3 init_db.py
```

This will:

- Create all tables using SQLAlchemy models
- Insert test users, places, amenities, and reviews
- Link data together (e.g., amenities to places, reviews to users)

#### 3. Visualize the data (optional but recommended)

To inspect your database, run [**sqlite-web**](https://github.com/coleifer/sqlite-web):

```bash
sqlite_web development.db
```

This will launch a web interface (default: [http://127.0.0.1:8080](http://127.0.0.1:8080)) where you can:

- View tables and data
- Run SQL queries
- Explore relationships

---

## ✅ Testing Checklist

- [ ] Login works and stores JWT in cookies
- [ ] List of places loads dynamically and filters work
- [ ] Details of a place are displayed correctly
- [ ] Add review form is conditionally rendered
- [ ] Reviews are submitted and confirmed
- [ ] Unauthenticated users are redirected properly

---

## 👨‍💻 Author

Project made by **Nicolas LASSOUANE**  
As part of the Holberton School curriculum (HBNB Project - Part 4)  
