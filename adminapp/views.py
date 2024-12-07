from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
def projecthomepage(request):
    return render(request, "adminapp/projecthomepage.html")
def registerpagecall(request):
    return render(request,'adminapp/register.html')
def loginpagecall(request):
    return render(request,'adminapp/login.html')
def loginpagelogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if len(username) != 4:
                messages.success(request, 'Login successful as Customer!')
                return redirect('customerapp:projecthomepage')  # Replace with your student homepage URL name

            elif len(username) == 4:
                # Redirect to FacultyHomePage
                # messages.success(request, 'Login successful as faculty!')
                return redirect('restaurantapp:projecthomepage')
            else:
                messages.error(request, 'Username length does not match customer or restaurant criteria.')
                return render(request, 'adminapp/login.html')
        else:
            # If authentication fails
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminapp/login.html')
    else:
        return render(request, 'adminapp/login.html')
def logout(request):
    auth.logout(request)
    return redirect('projecthomepage')
def registerpagelogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']  # Correct variable name (first_name)
        last_name = request.POST['lastname']  # Correct variable name (last_name)
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']

        try:
            if not username.isalpha():
                messages.info(request, 'Username must contain only alphabets.')
                return render(request, 'adminapp/register.html')
            if pass1 == pass2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'OOPS! Username already taken.')
                    return render(request, 'adminapp/register.html')

                # Check if email exists
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'OOPS! Email already registered.')
                    return render(request, 'adminapp/register.html')

                else:
                    # Create a new user
                    user = User.objects.create_user(
                        username=username,
                        password=pass1,
                        first_name=first_name,  # first_name variable
                        last_name=last_name,  # last_name variable
                        email=email
                    )
                    user.save()

                    messages.info(request, 'Account created Successfully!')
                    return render(request, 'adminapp/ProjectHomepage.html')

            else:
                messages.info(request, 'Passwords do not match.')
                return render(request, 'adminapp/register.html')

        except Exception as e:
            # Log any exception that occurs during user creation
            print(f"Error during user creation: {e}")
            messages.error(request, "An error occurred while creating your account.")
            return render(request, 'adminapp/register.html')

    else:
        return render(request, 'adminapp/register.html')
