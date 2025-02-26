from flask import Flask
from flask_restx import Api
from app.api.v1.amenities import api as amenities_ns

app = Flask(__name__)
api = Api(app, title="HBnB API", version="1.0", description="API for HBnB application")
api.add_namespace(amenities_ns, path="/amenities")
api.add_namespace(places_ns, path="/places") 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
