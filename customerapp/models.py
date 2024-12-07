from django.db import models
from restaurantapp.models import Item
from django.utils import timezone
from django.contrib.auth.models import User
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     order_date = models.DateTimeField(default=timezone.now)
#     address = models.TextField(max_length=255, default='No address provided')
#
#     def total_price(self):
#         return self.quantity * self.item.price
#
#     def __str__(self):
#         return f"Order by {self.user.username} - {self.item.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the item
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)  # Total price (quantity * item price)
    order_date = models.DateTimeField(default=timezone.now)
    address = models.TextField(max_length=255, default='No address provided')

    def __str__(self):
        return f"Order by {self.user.username} - {self.item.name}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The customer providing feedback
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # The item being reviewed
    comments = models.TextField()  # Customer's feedback comments
    rating = models.PositiveIntegerField()  # Rating out of 5
    feedback_date = models.DateTimeField(default=timezone.now)  # Timestamp of the feedback

    def _str_(self):
        return f"Feedback by {self.user.username} for {self.item.name}"