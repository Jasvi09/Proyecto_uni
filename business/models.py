from django.db import models
from administrator.models import User

# Create your models here.

list_service = (
    ("Impresión", "Impresión"),
    (("Arquitectura", "Arquitectura"))
)

class Services(models.Model):
    name = models.CharField(max_length=255, choices=list_service, default="Impresión")
    is_active = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_services')
    
    def __str__(self):
        return self.name + ' | ' + self.description + ' | ' + str(self.creation_date) + ' | ' + str(self.update_date)