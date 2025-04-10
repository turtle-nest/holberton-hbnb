from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'name': fields.String(required=True, description='Name of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'city': fields.String(required=True, description='City where the place is located'),
    'owner_id': fields.Integer(required=True, description='ID of the owner of the place'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

def serialize_place(place):
    """Convert Place object to a dictionary"""
    return {
        'id': place.id,
        'name': place.name,
        'description': place.description,
        'city': place.city,
        'owner_id': place.owner_id,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'price': place.price,
        'amenities': [amenity.id for amenity in place.amenities]
    }

repo = InMemoryRepository()

@api.route('/', methods=['GET', 'POST'])
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        facade = HBnBFacade()
        place_data = api.payload
        
        # Validate required fields
        if not place_data.get('name') or not place_data.get('description') or not place_data.get('city') or \
           not place_data.get('owner_id') or not place_data.get('latitude') or not place_data.get('longitude') or \
           not place_data.get('price'):
            return {"error": "Invalid input data"}, 400

        # Create place
        try:
            new_place = facade.create_place(place_data)
            return serialize_place(new_place), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        facade = HBnBFacade()
        places = facade.get_all_places()
        return [serialize_place(place) for place in places], 200

@api.route('/<place_id>', methods=['GET', 'PUT', 'DELETE'])
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        facade = HBnBFacade()
        place = facade.get_place(place_id)
        if place:
            return serialize_place(place), 200
        return {"error": "Place not found"}, 400

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        facade = HBnBFacade()
        place_data = api.payload
        
        # Validate required fields
        if not place_data.get('name') or not place_data.get('description') or not place_data.get('city') or \
           not place_data.get('owner_id') or not place_data.get('latitude') or not place_data.get('longitude') or \
           not place_data.get('price'):
            return {"error": "Invalid input data"}, 400
        
        # Update place
        updated_place = facade.update_place(place_id, place_data)
        if updated_place:
            return serialize_place(updated_place), 200
        return {"error": "Place not found"}, 400

    @api.response(204, 'Place deleted')
    def delete(self, place_id):
        """Delete a place given its identifier"""
        facade = HBnBFacade()
        facade.delete_place(place_id)
        return '', 204

# Export the namespace
places_ns = api
