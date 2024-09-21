import re
from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator, EmailValidator

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        if password and not self.is_valid_password(password):
            raise ValueError('Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def is_valid_password(self, password):
        return (len(password) >= 8 and
                re.search(r'[A-Z]', password) and  # At least one uppercase letter
                re.search(r'\d', password) and      # At least one digit
                re.search(r'[!@#$%^&*(),.?":{}|<>]', password))  # At least one special character

class User(AbstractBaseUser):
    id = models.ObjectIdField()  # Use ObjectIdField for MongoDB
    username = models.CharField(max_length=150, unique=True, validators=[MinLengthValidator(8)])
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    is_active = models.BooleanField(default=True)  # Field to track if user is active
    is_admin = models.BooleanField(default=False)   # Field to track admin status
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()  # Associate UserManager with User

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        """Return True if the user is a staff member."""
        return self.is_admin
