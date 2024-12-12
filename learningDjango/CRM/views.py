from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Home view for handling both authenticated and unauthenticated users
def home(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user})

    # Handle login for unauthenticated users
    if request.method == "POST":  
        username = request.POST["username"]  
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return redirect('home')  # Redirect to the home view after successful login
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'home.html', {})  # Render the home page with login form if not logged in

# Logout view to handle user logout
def logout_user(request):
    logout(request)  # Logout the user
    messages.success(request, "You have successfully logged out")  # Show logout success message
    return redirect('home')  # Redirect to home page after logout
