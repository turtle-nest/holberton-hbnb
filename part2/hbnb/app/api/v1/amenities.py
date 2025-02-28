from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from datetime import datetime
from app.persistence.repository import InMemoryRepository

amenities_ns = Namespace('amenities', description='Amenity operations')

amenity_model = amenities_ns.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

def serialize_amenity(amenity):
    """Convert Amenity object to a dictionary and handle datetime serialization"""
    amenity_dict = amenity.__dict__.copy()
    for key, value in amenity_dict.items():
        if isinstance(value, datetime):
            amenity_dict[key] = value.isoformat()
    return amenity_dict

repo = InMemoryRepository()

@amenities_ns.route('/')
class AmenityList(Resource):
    @amenities_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = HBnBFacade().get_all_amenities()
        return [serialize_amenity(amenity) for amenity in amenities], 200

    @amenities_ns.expect(amenity_model)
    @amenities_ns.response(201, 'Amenity successfully created')
    @amenities_ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = amenities_ns.payload
        name = data.get("name", "").strip()
        if not name:
            return {"error": "Name is required"}, 400

        new_amenity = HBnBFacade().create_amenity({"name": name})
        return serialize_amenity(new_amenity), 201

@amenities_ns.route('/<int:amenity_id>')
class AmenityResource(Resource):
    @amenities_ns.response(200, 'Amenity details retrieved successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = HBnBFacade().get_amenity(amenity_id)
        if amenity:
            return serialize_amenity(amenity), 200
        return {"error": "Amenity not found"}, 404

    @amenities_ns.expect(amenity_model)
    @amenities_ns.response(200, 'Amenity updated successfully')
    @amenities_ns.response(404, 'Amenity not found')
    @amenities_ns.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = amenities_ns.payload
        name = data.get("name", "").strip()
        if not name:
            return {"error": "Name is required"}, 400

        update_amenity = HBnBFacade().update_amenity(amenity_id, {"name": name})
        if update_amenity:
            return {"message": "Amenity updated successfully"}, 200
        return {"error": "Amenity not found"}, 404
