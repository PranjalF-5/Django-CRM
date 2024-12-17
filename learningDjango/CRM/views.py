from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.crypto import get_random_string
from .forms import UserRegistrationForm, PasswordResetRequestForm, RecordForm
from .models import OTP
from django.utils import timezone
from .models import Record
# Home view for handling both authenticated and unauthenticated users
def home(request):
    # Check if the user is already authenticated
    records = Record.objects.all()
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user, 'records':records})

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

# Register user and send confirmation email
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Send confirmation email
            send_mail(
                'Account Registration Successful',
                f'Hello {username},\n\nYour account has been successfully created!',
                'from@example.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            
            messages.success(request, "Account successfully created! A confirmation email has been sent.")
            return redirect('home')  # Redirect to the home page after successful registration
        else:
            messages.error(request, "There was an error with your submission. Please check the fields and try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

# Password reset request with OTP sent via email
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                
                # Generate OTP
                otp = get_random_string(length=6, allowed_chars='0123456789')
                expires_at = timezone.now() + timezone.timedelta(minutes=3)  # OTP expires in 10 minutes

                # Store OTP in the OTP model
                OTP.objects.create(user=user, otp=otp, expires_at=expires_at)

                # Send OTP to user's email
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    'pranjalmayank555@gmail.com',  # Replace with your actual email
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "OTP sent to your email. Please check.")
                return redirect('password_reset_verify')
            except User.DoesNotExist:
                messages.error(request, "No user found with that email address.")
                return redirect('password_reset_request')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})

# Password reset verification (using OTP)
def password_reset_verify(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        try:
            # Retrieve OTP record based on the OTP entered by the user
            otp_record = OTP.objects.get(otp=otp)

            # Check if the OTP is expired
            if otp_record.is_expired():
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect('password_reset_request')

            # OTP is valid, allow the user to reset their password
            if 'new_password' in request.POST and 'confirm_password' in request.POST:
                new_password = request.POST['new_password']
                confirm_password = request.POST['confirm_password']

                # Check if the passwords match
                if new_password != confirm_password:
                    messages.error(request, "Passwords do not match. Please try again.")
                    return redirect('password_reset_verify')

                user = otp_record.user
                user.set_password(new_password)
                user.save()

                # Invalidate the OTP after use
                otp_record.delete()

                messages.success(request, "Your password has been reset successfully.")
                return redirect('home')  # Redirect after password reset

        except OTP.DoesNotExist:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('password_reset_verify')

    return render(request, 'password_reset_verify.html')



 #adding the individual customer

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Show the record with the primary key
        customer_record = Record.objects.get(id=pk)  # Use 'pk', not 'id'
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request,'You must be logged in to view the records')
        return redirect('home')  # Redirect to login if not authenticated


    

#delete Records

def delete_record(request, id):
    if request.user.is_authenticated:
            if request.method == 'POST':
                record = get_object_or_404(Record, id=id)
                record.delete()
                messages.success(request, "Record successfully Deleted")
                return redirect('home')  # Redirect to the home page after deletion
    else:
        messages.success("You must be logged in to delete")
        return redirect('home')
    


# Add new Record
def new_record(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RecordForm(request.POST)
            if form.is_valid():
                form.save()  # Save the form data to the database
                return redirect('home')  # Redirect after successful submission
        else:
            form = RecordForm()

        return render(request, 'new_record.html', {'form': form})

    else:
        messages.error(request, "Please log in to add records.")
        return redirect('home') 