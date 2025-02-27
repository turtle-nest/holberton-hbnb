from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')


amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = HBnBFacade.get_all_amenities()
        return amenities, 200

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload
        name = data.get("name", "").strip()
        if not name:
            return {"error": "Name is required"}, 400

        new_amenity = HBnBFacade.create_amenity({"name": name})
        return new_amenity, 201


@api.route('/<int:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = HBnBFacade.get_amenity_by_id(amenity_id)
        if amenity:
            return amenity, 200
        return {"error": "Amenity not found"}, 404

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload
        name = data.get("name", "").strip()
        if not name:
            return {"error": "Name is required"}, 400

        update_amenity = HBnBFacade.update_amenity(amenity_id, {"name": name})
        if update_amenity:
            return update_amenity, 200
        return {"error": "Amenity not found"}, 404
