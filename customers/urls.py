from django.urls import path
from . import views
# from views import main

urlpatterns = [
    path('',views.main , name="main"),
    path('menu/',views.menu , name="menu"),
    path('login/',views.login_user , name="login"),
    path('signup/',views.signup , name="signup"),
    path('logout/',views.logout_user , name="logout"),
    path('users/<str:username>/<int:id>/edit/', views.edit_user, name="edit-user"),
    path('show-cart/',views.show_cart , name="show-cart"),
    path('delete-item-in-cart/<int:id>/<str:item_name>/delete/',views.delete_item_in_cart , name="delete-item-in-cart"),
    path('show-delivery/<int:id>/',views.show_delivery , name="show-delivery"),
    path('order-history/',views.order_history , name="order-history"),
    path('show-category/<str:category_name>/<int:id>/',views.show_category , name="show-category")
]
