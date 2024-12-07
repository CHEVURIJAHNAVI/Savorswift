from django.contrib.auth.models import User
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='item_images/')
    price=models.BigIntegerField(default=0)
    description = models.TextField()
    restaurant_user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

