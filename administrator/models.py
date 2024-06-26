from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    identification_document = models.CharField(
        max_length=8, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        BUSINESS = "BUSINESS", "Business"
        CUSTOMER = "CUSTOMER", "Customer"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class Customer(User):
    base_role = User.Role.CUSTOMER

    class Meta:
        proxy = True


class Business(User):
    base_role = User.Role.BUSINESS

    class Meta:
        proxy = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    data_full = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
