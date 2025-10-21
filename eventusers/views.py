from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import users

# Show Login Page
def show_login(request):
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Replace 'home' with your homepage URL name
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'main.html')  # login page template


# Show Signup Page
def show_account(request):
    if request.method == 'POST' and 'register' in request.POST:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            # Create user with hashed password
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # Add extra info in your custom users table
            users.objects.create(
                user=user,
                phone=phone,
                address=address
            )

            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')  # Make sure this is your login URL name
        except Exception as e:
            messages.error(request, "Duplicate username or invalid credentials.")

    return render(request, 'signup.html')  # signup page template


# Logout function (optional)
def logout_view(request):
    auth_logout(request)
    return redirect('login')
