from django.db import models

# restaurant
class Category (models.Model):
    name = models.CharField(max_length=200, blank=False)
    image = models.CharField(max_length=200, blank=False)

    def __str__(self) -> str:
        return self.name

class Dish (models.Model):
    dish_name = models.CharField(max_length=200, blank=False)
    price = models.IntegerField(blank=False)
    description = models.CharField(max_length=200, blank=False)
    image = models.CharField(max_length=200, blank=False)
    is_gluten_free = models.BooleanField (default=False)
    is_vegeterian = models.BooleanField (default=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)  
    
    def __str__(self) -> str:
        return self.dish_name