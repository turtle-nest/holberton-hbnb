from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app import db

class UserRepository(SQLAlchemyRepository):
    """
    UserRepository extends the base SQLAlchemyRepository to provide
    specialized methods for interacting with the User model.
    """

    def __init__(self):
        """
        Initializes the UserRepository with the User model.
        This leverages all CRUD methods from the parent SQLAlchemyRepository.
        """
        self.session = db.session
        super().__init__(User)

    def add(self, user):
        """
        Add a new user to the database and commit the transaction.

        This method takes a User object, adds it to the current SQLAlchemy session,
        and commits the changes to persist the user in the database.
        """
        self.session.add(user)
        self.session.commit()


    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.add(user)
        return user


    def get_user_by_email(self, email):
        """
        Retrieves a user from the database by email.
        """
        return self.model.query.filter_by(email=email).first()
