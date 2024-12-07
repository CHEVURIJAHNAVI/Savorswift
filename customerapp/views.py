from django.core.mail import send_mail
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

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'customerapp/wishlist.html', {'wishlist_items': wishlist_items})
# def payment_view(request):
#     if request.method == 'POST':
#         upi_id = request.POST.get('upi_id')
#         return render(request,'payment_success')
#     return HttpResponse("Invalid request")
def orderhistory(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'customerapp/order_history.html', {'orders': orders})
from customerapp.models import Wishlist,Order
from .forms import OrderItemForm
def place_order(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            action = form.cleaned_data['action']
            total_price = item.price * quantity
            if action == 'wishlist':
                wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, item=item)
                if created:
                    pass
                else:
                    message = "Item is already in your wishlist."
                return redirect('customerapp:wishlist')
            elif action == 'buy':
                order = Order.objects.create(
                    user=request.user, item=item, quantity=quantity,
                    price=item.price, total_price=total_price  # Store total_price here
                )
                order.save()
                subject = 'SavorSwift - Order Placed'
                message = f'Hello, {request.user.first_name} {request.user.last_name}. Your order for {item.name} has been placed with a total cost of {total_price}. Thank you for choosing us.'
                from_email = 'saisreerachapudi@gmail.com'
                recipient_list = [request.user.email]
                send_mail(subject, message, from_email, recipient_list)
                return redirect('customerapp:checkout')
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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Feedback, Item
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def give_feedback(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user = request.user
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = user
            feedback.item = item
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('customerapp:item_reviews')  # Redirect to reviews page
    else:
        form = FeedbackForm()
    return render(request, 'customerapp/give_feedback.html', {'form': form, 'item': item, 'user': user})

def display_reviews(request):
    feedbacks = Feedback.objects.all().order_by('-feedback_date')  # Fetch all feedback
    return render(request, 'customerapp/item_reviews.html', {'feedbacks': feedbacks})
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order  # Assuming you have an Order model for storing order details.
from django.contrib import messages


# Payment view to handle the checkout form and processing
def payment_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('customerapp:checkout')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if payment_method == 'upi':
            upi_id = request.POST.get('upi_id')
            if not upi_id:
                messages.error(request, "UPI ID is required.")
                return redirect('customerapp:checkout')
            return render(request, 'customerapp/payment_successful.html')

        elif payment_method == 'credit_card':
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')
            if not (card_number and expiry_date and cvv):
                messages.error(request, "All credit card fields are required.")
                return redirect('customerapp:checkout')
            messages.success(request, "Payment successful via Credit Card!")
            return render(request, 'customerapp/payment_successful.html')

        else:
            messages.error(request, "Invalid payment method selected.")
            return redirect('customerapp:checkout')

    else:
        total_price = order.item.price * order.quantity  # Calculate total price
        return render(request, 'customerapp/checkout.html', {
            'order': order,
            'total_price': total_price,
        })

def order_success_view(request):
    return render(request, 'customerapp/payment_successful.html')  # This is the success page to show after payment