from django.urls import path,include
from . import views
app_name='customerapp'
urlpatterns = [
    path('',views.projecthomepage,name='projecthomepage'),
    path('changepasswordpagecall/',views.changepasswordpagecall,name='changepasswordpagecall'),
    path('earningspagecall/',views.earningspagecall,name='earningspagecall'),
    path('editprofilepagecall/',views.editprofilepagecall,name='editprofilepagecall'),
    path('viewprofilepagecall/',views.viewprofilepagecall,name='viewprofilepagecall'),
    path('notificationspagecall/',views.notificationspagecall,name='notificationspagecall'),
    path('dashboardpagecall/',views.dashboardpagecall,name='dashboardpagecall'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurant_items/',views.restaurant_items,name='restaurant_items'),
path('restaurants/<int:restaurant_id>/explore/', views.restaurant_items, name='restaurant_items'),
    path('restaurants/<int:restaurant_id>/items/', views.restaurant_items, name='restaurant_items'),
    path('place_order/<int:item_id>/', views.place_order, name='place_order'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
path('orderhistory/', views.orderhistory, name='orderhistory'),
path('payment/', views.payment_view, name='payment'),


]
