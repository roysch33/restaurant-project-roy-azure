from django.urls import path
from . import views
# from views import main

urlpatterns = [
    path('manager-signup/',views.manager_signup, name="manager-signup"),
    path('manager-page/',views.manager_page, name="manager-page"),
    path('manager-deliveries/',views.manager_deliveries, name="manager-deliveries"),
    path('manager-categories/',views.manager_categories, name="manager-categories"),
    path('edit-category/<str:category_name>/<int:id>/',views.edit_category, name="edit-category"),
    path('add-category/',views.add_category, name="add-category"),
    path('delete_category/<str:category_name>/<int:id>/',views.delete_category, name="delete-category"),
    path('show-dishes/<str:category_name>/<int:id>/',views.show_dishes, name="show-dishes"),
    path('edit-dish/<str:dish_name>/<int:id>/',views.edit_dish, name="edit-dish"),
    path('add-dish/',views.add_dish, name="add-dish"),
    path('delete_dish/<str:dish_name>/<int:id>/',views.delete_dish, name="delete-dish")
]