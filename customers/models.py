from django.db import models
from django.contrib.auth.models import User
from management.models import Dish

# customers
class Cart (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  

    class Meta:
        db_table = "cart"

    def __str__(self) -> str:
        return f"cart's id:{self.pk}, the user: {self.user_id}"


class Item (models.Model):
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)  
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    amount = models.IntegerField(blank=False)

    class Meta:
        db_table = "item"


class Delivery (models.Model):
    order_id = models.OneToOneField(Cart, on_delete=models.CASCADE, primary_key=True)
    is_delivered = models.BooleanField (default=False)
    address = models.CharField(max_length=200, blank=False)
    comment = models.CharField(max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "delivery"




