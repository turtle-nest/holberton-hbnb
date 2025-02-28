from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from app.persistence.repository import InMemoryRepository

reviews_ns = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = reviews_ns.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

def serialize_review(review):
    """Convert Review object to a dictionary"""
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user_id,
        'place_id': review.place_id,
        'created_at': review.created_at.isoformat(),
        'updated_at': review.updated_at.isoformat()
    }

repo = InMemoryRepository()

@reviews_ns.route('/')
class ReviewList(Resource):
    @reviews_ns.expect(review_model)
    @reviews_ns.response(201, 'Review successfully created')
    @reviews_ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = request.json
        review = facade.create_review(data)
        if review:
            return serialize_review(review), 201
        return {'message': 'Invalid input data'}, 400

    @reviews_ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [serialize_review(review) for review in reviews], 200

@reviews_ns.route('/<review_id>')
class ReviewResource(Resource):
    @reviews_ns.response(200, 'Review details retrieved successfully')
    @reviews_ns.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review_by_id(review_id)
        if review:
            return serialize_review(review), 200
        return {'message': 'Review not found'}, 404

    @reviews_ns.expect(review_model)
    @reviews_ns.response(200, 'Review updated successfully')
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = request.json
        updated_review = facade.update_review(review_id, data)
        if updated_review:
            return serialize_review(updated_review), 200
        return {'message': 'Review not found'}, 404

    @reviews_ns.response(200, 'Review deleted successfully')
    @reviews_ns.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}, 200
        return {'message': 'Review not found'}, 404

@reviews_ns.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @reviews_ns.response(200, 'List of reviews for the place retrieved successfully')
    @reviews_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is not None:
            return [serialize_review(review) for review in reviews], 200
        return {'message': 'Place not found'}, 404
