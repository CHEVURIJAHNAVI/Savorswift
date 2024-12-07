from django.urls import path, include
from . import views
app_name='restaurantapp'
urlpatterns = [
    path('', views.projecthomepage, name='projecthomepage'),
    path('items/', views.item_list, name='item_list'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('delete/success/<int:item_id>/', views.delete_success, name='delete_success'),
    path('viewprofilepagecall/', views.viewprofilepagecall, name='viewprofilepagecall'),
    path('editprofilepagecall/', views.editprofilepagecall, name='editprofilepagecall'),
    path('changepasswordpagecall/', views.changepasswordpagecall, name='changepasswordpagecall'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('changepasswordpagelogic/', views.changepasswordpagelogic, name='changepasswordpagelogic'),
    path('restaurant/orders/', views.restaurant_orders, name='restaurant_orders'),
path('item-reviews/', views.display_item_reviews, name='item_reviews'),
path('orders/', views.display_restaurant_orders, name='display_restaurant_orders'),
]