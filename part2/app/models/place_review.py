import datetime

class PlaceReview:
    """Class that represents a review for a place"""
    
    def __init__(self, review_text, rating, user_id):
        self.review_text = review_text
        self.rating = rating
        self.user_id = user_id
        self.date = datetime.datetime.now()

    def __repr__(self):
        return f"<PlaceReview (user_id={self.user_id}, rating={self.rating})>"
