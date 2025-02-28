from app.models.base_model import BaseModel

class User(BaseModel):
    """User class that inherits from BaseModel.
    Represents a user with first name, last name, email, and password.
    """
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a new User instance."""
        super().__init__()
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._is_admin = is_admin

    @property
    def first_name(self):
        """Get the user's first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Set the user's first name."""
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        if not value.strip():
            raise ValueError("First name cannot be empty")
        self._first_name = value

    @property
    def last_name(self):
        """Get the user's last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Set the user's last name."""
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        if not value.strip():
            raise ValueError("Last name cannot be empty")
        self._last_name = value

    @property
    def email(self):
        """Get the user's email address."""
        return self._email

    @email.setter
    def email(self, value):
        """Set the user's email address."""
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        self._email = value

    @property
    def password(self):
        """Get the user's password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set the user's password."""
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self._password = value
