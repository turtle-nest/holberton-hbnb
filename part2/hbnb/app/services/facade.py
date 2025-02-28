from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
"""Module that contains the HBnBfacade class"""

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()


    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user


    def create_amenity(self, amenity_data):
        """
        Create a new amenity and add it to the amenity repository
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        """
        Retrieve a single amenity by its unique ID
        """
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        """
        Retrieve all amenities from the amenity repository
        """
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity with new data
        """
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
        return amenity


    def create_place(self, place_data):
        """
        Create a new place and add it to the place repository
        """
        place = Place(**place_data)
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        """
        Retrieve a single place by its unique ID
        """
        return self.place_repo.get(place_id)


    def get_all_places(self):
        """
        Retrieve all places from the place repository
        """
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        """
        Update an existing place with new data
        """
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
        return place


    def get_all_users(self):
        users = self.user_repo.get_all("users")
        return [{k: v for k, v in user.items() if k != "password"} for user in users]


    def update_user(self, user_id, data):
        """Update an existant user"""
        user = self.user_repo.update("users", user_id, data)
        if user:
            return {k: v for k, v in user.items() if k != "password"}
        return None


    def create_review(self, review_data):
        """Create a new review and add it to the review repository"""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review


    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()


    def get_review_by_id(self, review_id):
        """Retrieve a review by its ID"""
        return self.review_repo.get_by_id(review_id)


    def update_review(self, review_id, review_data):
        """Update a review's information"""
        review = self.review_repo.get_by_id(review_id)
        if review:
            for key, value in review_data.items():
                setattr(review, key, value)
            self.review_repo.update(review)
            return review
        return None


    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get_by_id(review_id)
        if review:
            self.review_repo.delete(review)
            return True
        return False


    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        return self.review_repo.get_by_place_id(place_id)
