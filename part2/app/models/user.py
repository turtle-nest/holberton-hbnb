from app.models.base_model import BaseModel

class User(BaseModel):
    """User class that inherits from BaseModel.
    Represents a user with first name, last name, email, and password.
    """
    # Class-level attribute to store emails for uniqueness check
    _existing_emails = set()  # Using a set to store emails

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a new User instance."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

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
        if len(value) > 50:
            raise ValueError("First name cannot be longer than 50 characters")
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
        if len(value) > 50:
            raise ValueError("Last name cannot be longer than 50 characters")
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
        if not self.is_email_unique(value):
            raise ValueError("Email must be unique")
        self._email = value
        # Add the email to the set of existing emails once it's successfully set
        User._existing_emails.add(value)

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

    @property
    def is_admin(self):
        """Get whether the user is an admin."""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """Set whether the user is an admin."""
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean value")
        self._is_admin = value

    def is_email_unique(self, email):
        """Check if the email is unique by looking up in the set of existing emails."""
        return email not in User._existing_emails
