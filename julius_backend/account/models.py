from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

ROLE_CHOICES = [(0, "USER"), (1, "ADMIN")]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **otherfields):
        """
        Creates and saves a User with the given email, name, tc and password.
        """

        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            email = self.normalize_email("email"),
            first_name = otherfields.get("first_name"),
            last_name = otherfields.get("last_name", None),
            date_of_birth = otherfields.get("date_of_birth"),
            phone_number = otherfields.get("phone_number", None),
            role = otherfields.get("role", 0),
            subscription_start_date = otherfields.get("subscription_start_date", None),
            subscription_end_date = otherfields.get("subscription_end_date", None),
            status = otherfields.get("status", True)
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user


class Subscription(models.Model):
    '''
        Creates types and price of the subscriptions
        available
    '''
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    day = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'subscription'
        ordering = ['-created_at']



class User(AbstractBaseUser):
    '''
        Creats abstract user for authentication and login with 
        email address login fields and all other necessary fields
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null = True, blank = True)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length = 10)
    role = models.IntegerField(choices=ROLE_CHOICES, default = 0)
    subscription_id = models.ForeignKey(Subscription, db_column = "subscription_id", on_delete=models.CASCADE, null = True, blank = True)
    subscription_start_date = models.DateTimeField(null = True, blank = True)
    subscription_end_date = models.DateTimeField(null = True, blank = True)
    status = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted_at = models.DateTimeField(null = True, blank = True)

    USERNAME_FIELD = "email"
    
    class Meta:
        db_table = 'user'
        ordering = ['-created_at']
    



