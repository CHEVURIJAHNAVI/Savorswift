from django.shortcuts import render
# Create your views here.
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import ItemForm
from django.shortcuts import get_object_or_404
from .models import Item
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
def projecthomepage(request):
    return render(request, "restaurantapp/projecthomepage.html")

def home(request):
    return render(request, 'restaurantapp/Homepage.html')
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('restaurantapp:item_list'))
    else:
        form = ItemForm(instance=item)
    return render(request, 'restaurantapp/edit_item.html', {'form': form, 'item': item})

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item successfully deleted!')
        return redirect('restaurantapp:delete_success', item_id=item.id)

    return render(request, 'restaurantapp/delete_item.html', {'item': item})
def delete_success(request, item_id):
    return render(request, 'restaurantapp/delete_success.html', {'item_id': item_id})
def editprofilepagecall(request):
    return render(request,'restaurantapp/editprofile.html')
def viewprofilepagecall(request):
    return render(request,'restaurantapp/viewprofile.html')
@login_required  # Ensure that only logged-in users can add items
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Manually set the restaurant_user field
            item = form.save(commit=False)  # Don't save the object yet
            item.restaurant_user = request.user  # Assign the logged-in user
            item.save()  # Now save the item with the restaurant_user set
            return redirect('restaurantapp:item_list')  # Redirect after saving
    else:
        form = ItemForm()

    return render(request, 'restaurantapp/add_item.html', {'form': form})
def item_list(request):
    items = Item.objects.filter(restaurant_user=request.user)
    return render(request, 'restaurantapp/item_list.html', {'items': items})
def changepasswordpagecall(request):
    return render(request,'restaurantapp/changepassword.html')

@login_required
def changepasswordpagelogic(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')  # Safely access POST data
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        # Ensure the user is authenticated
        user = authenticate(username=request.user.username, password=old_password)
        if user is not None:
            if new_password1 == new_password2:
                # Set the new password
                user.set_password(new_password1)
                user.save()

                # Update session to prevent logging out after password change
                update_session_auth_hash(request, user)
                return redirect('logout')  # Redirect to a success page
            else:
                messages.info(request, 'New passwords do not match.')
                return render(request, 'restaurantapp/changepassword.html')
        else:
            messages.info(request, 'Old password is incorrect.')
            return render(request, 'restaurantapp/changepassword.html')
    else:
        return render(request, 'restaurantapp/changepassword.html')
@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        try:
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
        except:
            messages.error(request, 'An error occurred while updating your profile. Please try again.')

        return redirect('logout')

    return render(request, 'restaurantapp/editprofile.html')

# restaurantapp/views.py

from django.shortcuts import render
from restaurantapp.models import Item
from django.contrib.auth.decorators import login_required

@login_required
def restaurant_orders(request):
    # Get the restaurant's items
    items = Item.objects.filter(restaurant_user=request.user)

    # Get orders for those items
    orders = Order.objects.filter(item__in=items)

    return render(request, 'restaurantapp/restaurant_orders.html', {'orders': orders})
