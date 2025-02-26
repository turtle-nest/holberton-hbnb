import sys
import os
from flask import Flask
from app.api.v1 import bp

project_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_path)
sys.path.append(os.path.join(project_path, "app"))

print("Flask API is starting...")

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == "__main__":
    print("Running Flask on http://127.0.0.1:5000")
    app.run(debug=True)
