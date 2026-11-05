from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages
from .models import Tenant, TenantProfile

User = get_user_model()


def register_tenant(request):
    """Handles tenant registration."""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'tenant/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return render(request, 'tenant/register.html')

        # Create User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Create Tenant
        tenant = Tenant.objects.create(user=user)

        # Create TenantProfile
        profile = TenantProfile.objects.create(
            user=user,
            full_name=full_name,
            phone_number=phone_number
        )

        # Log the user in
        login(request, user)
        messages.success(request, "Registration successful! Welcome to our platform.")
        return redirect('tenant:dashboard')

    return render(request, 'tenant/register.html')


def login_tenant(request):
    """Handles tenant login."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('tenant:dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'tenant/login.html')

    return render(request, 'tenant/login.html')


def tenant_dashboard(request):
    """Displays the tenant dashboard."""
    return render(request, 'tenant/dashboard.html')