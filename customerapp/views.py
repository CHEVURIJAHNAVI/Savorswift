from django.http import HttpResponse
from .models import Wishlist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def projecthomepage(request):
    return render(request, "customerapp/projecthomepage.html")

def editprofilepagecall(request):
    return render(request,'customerapp/editprofile.html')
def viewprofilepagecall(request):
    return render(request,'customerapp/viewprofile.html')
def notificationspagecall(request):
    return render(request,'customerapp/notifications.html')
def dashboardpagecall(request):
    return render(request,'customerapp/dashboard.html')
def earningspagecall(request):
    return render(request,'customerapp/earnings.html')
def changepasswordpagecall(request):
    return render(request,'customerapp/changepassword.html')
from django.db.models.functions import Length
def restaurant_list(request):
    restaurants = User.objects.annotate(username_length=Length('username')).filter(username_length=4)
    return render(request, 'customerapp/restaurantslist.html', {'restaurants': restaurants})
@login_required
def restaurant_items(request, restaurant_id):
    restaurant = get_object_or_404(User, id=restaurant_id)
    if len(restaurant.username) != 4:
        return render(request, 'customerapp/restaurantitems.html', {'error': 'Invalid restaurant'})
    items = Item.objects.filter(restaurant_user=restaurant)  # Adjust field name to match your model

    return render(request, 'customerapp/restaurantitems.html', {'restaurant': restaurant, 'items': items})

from django.shortcuts import render, get_object_or_404, redirect
from restaurantapp.models import Item
from customerapp.models import (Wishlist, Order)
from .forms import OrderItemForm

# def place_order(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#
#     if request.method == 'POST':
#         form = OrderItemForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             action = form.cleaned_data['action']
#             if action == 'wishlist':
#                 wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, item=item)
#                 if created:
#                     message = "Item added to wishlist."
#                 else:
#                     message = "Item is already in your wishlist."
#                 return redirect('customerapp:wishlist')
#             elif action == 'buy':
#                 order = Order.objects.create(user=request.user, item=item, quantity=quantity,
#                                              price=item.price * quantity)
#                 order.save()
#                 return redirect('customerapp:checkout',)
#
#             return redirect('restaurantapp:restaurant_items',
#                             restaurant_id=item.restaurant_user.id)
#     else:
#         form = OrderItemForm()
#     return render(request, 'customerapp/placeorder.html', {'item': item, 'form': form})
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'customerapp/wishlist.html', {'wishlist_items': wishlist_items})

# @login_required
# def checkout(request):
#     return render(request, 'customerapp/checkout.html')
def payment_view(request):
    if request.method == 'POST':
        upi_id = request.POST.get('upi_id')
        return HttpResponse(f"Payment processed for UPI ID: {upi_id}")
    return HttpResponse("Invalid request")
def orderhistory(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'customerapp/order_history.html', {'orders': orders})
from django.shortcuts import render, get_object_or_404, redirect
from restaurantapp.models import Item
from customerapp.models import Wishlist, Order
from .forms import OrderItemForm

def place_order(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            action = form.cleaned_data['action']
            total_price = item.price * quantity  # Calculate total price

            if action == 'wishlist':
                wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, item=item)
                if created:
                    message = "Item added to wishlist."
                else:
                    message = "Item is already in your wishlist."
                return redirect('customerapp:wishlist')

            elif action == 'buy':
                # Create the order with the total price
                order = Order.objects.create(user=request.user, item=item, quantity=quantity,
                                             price=item.price, total_price=total_price)  # Store total_price here
                order.save()
                return redirect('customerapp:checkout',)

            return redirect('restaurantapp:restaurant_items', restaurant_id=item.restaurant_user.id)
    else:
        form = OrderItemForm()
    return render(request, 'customerapp/placeorder.html', {'item': item, 'form': form})


@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user).last()
    total_price = order.item.price * order.quantity
    if not order:
        return redirect('customerapp:order_history')
    return render(request, 'customerapp/checkout.html', {'order': order,'total_price': total_price})
