from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # Ensure backend attribute is set on user object for multiple backends support
            if not hasattr(user, 'backend'):
                user.backend = 'django.contrib.auth.backends.ModelBackend'
            # Specify backend explicitly to avoid multiple backends error
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'You are now logged in.')
            
            # Check if there's a next parameter in the request
            next_url = request.POST.get('next', '')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    # Set backend attribute on user object for multiple backends support
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    # Specify backend explicitly to avoid multiple backends error
                    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, 'You are now registered and logged in.')
                    return redirect('dashboard')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


@login_required(login_url = 'login')
def dashboard(request):
    # Filter contacts by user_id for authenticated users
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    
    # Debug logging
    print(f"🔍 Dashboard for user ID: {request.user.id}")
    print(f"🔍 User email: {request.user.email}")
    print(f"🔍 Found {user_inquiry.count()} inquiries for this user")
    
    # Log some details about found inquiries
    for inquiry in user_inquiry[:5]:  # Show first 5
        print(f"   - Inquiry ID: {inquiry.id}, Car: {inquiry.car_title}, Date: {inquiry.create_date}")
    
    data = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')
