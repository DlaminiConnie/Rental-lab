from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Landlord, LandlordProfile
from rooms.models import Room, RoomPhoto

User = get_user_model()


# =========================================================
# 1. LANDLORD REGISTRATION
# =========================================================

def register_landlord(request):
    """
    View to handle landlord registration.
    GET  : Shows the registration form.
    POST : Processes the registration data and creates a new landlord account.
    """
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        id_document = request.FILES.get('id_document')
        selfie_photo = request.FILES.get('selfie_photo')

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'landlord/register.html')

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'landlord/register.html')

        # Create the user account
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Create landlord record
        Landlord.objects.create(
            user=user,
            verification_status='pending'
        )

        # Create landlord profile record
        LandlordProfile.objects.create(
            user=user,
            full_name=full_name,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            id_document_path=id_document.name if id_document else '',
            selfie_photo_path=selfie_photo.name if selfie_photo else '',
        )

        # Notify admin
        try:
            send_mail(
                subject="New Landlord Registration Pending Approval",
                message=f"A new landlord has registered.\n\n"
                        f"Name: {full_name}\n"
                        f"Email: {email}\n"
                        f"Phone: {phone_number}\n\n"
                        f"Please log in to the admin panel to approve or reject.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, "Registration successful. Please wait for admin approval.")
        return redirect('landlord:login')

    return render(request, 'landlord/register.html')


# =========================================================
# 2. LANDLORD LOGIN
# =========================================================

def login_landlord(request):
    """
    View to handle landlord login.
    GET  : Shows the login form.
    POST : Authenticates the user and logs them in if credentials are valid.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('landlord:dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'landlord/login.html')

    return render(request, 'landlord/login.html')


# =========================================================
# 3. LANDLORD DASHBOARD
# =========================================================

@login_required
def landlord_dashboard(request):
    """
    Displays the landlord dashboard with stats.
    """
    # Ensure user is a landlord
    if not hasattr(request.user, 'landlord'):
        messages.error(request, "You are not registered as a landlord.")
        return redirect('landlord:register')

    rooms = Room.objects.filter(landlord=request.user)

    total_rooms = rooms.count()
    pending_rooms = rooms.filter(status='pending').count()
    approved_rooms = rooms.filter(status='approved').count()

    context = {
        'total_rooms': total_rooms,
        'pending_rooms': pending_rooms,
        'approved_rooms': approved_rooms,
        'unread_messages': 0,  # Placeholder for chat system
    }

    return render(request, 'landlord/dashboard.html', context)


# =========================================================
# 4. POST A ROOM
# =========================================================

@login_required
def post_room(request):
    """
    Allows verified landlords to post a new room.
    Room is created with status 'pending' awaiting admin approval.
    """
    # Ensure user is a verified landlord
    if not hasattr(request.user, 'landlord') or request.user.landlord.verification_status != 'verified':
        messages.error(request, "You must be a verified landlord to post rooms.")
        return redirect('landlord:dashboard')

    if request.method == 'POST':
        price = request.POST.get('price')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')
        bedrooms = request.POST.get('bedrooms')
        description = request.POST.get('description')
        availability_date = request.POST.get('availability_date')
        affidavit = request.FILES.get('affidavit')

        # Validate required fields
        if not all([price, address, city, province, bedrooms]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'landlord/post_room.html')

        # Create the room with status 'pending'
        room = Room.objects.create(
            landlord=request.user,
            price=price,
            address=address,
            city=city,
            province=province,
            postal_code=postal_code,
            bedrooms=bedrooms,
            description=description,
            availability_date=availability_date or None,
            affidavit_path=affidavit.name if affidavit else '',
            status='pending',
        )

        # Handle photo uploads
        photos = request.FILES.getlist('photos')
        for index, photo in enumerate(photos):
            RoomPhoto.objects.create(
                room=room,
                image_path=photo.name,
                display_order=index,
            )

        # Notify admin by email
        try:
            send_mail(
                subject=f"New Room Pending Approval: {room.address}",
                message=f"A new room has been posted by {request.user.email}.\n\n"
                        f"Address: {room.address}, {room.city}, {room.province}\n"
                        f"Price: R{room.price}\n"
                        f"Bedrooms: {room.bedrooms}\n\n"
                        f"Please log in to the admin panel to approve or reject it.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(
            request,
            "Room posted successfully! It is now pending admin approval. "
            "You will be notified once it is approved."
        )
        return redirect('landlord:dashboard')

    return render(request, 'landlord/post_room.html')


# =========================================================
# 5. MY LISTINGS
# =========================================================

@login_required
def my_listings(request):
    """
    Displays all rooms posted by the logged-in landlord.
    """
    if not hasattr(request.user, 'landlord'):
        messages.error(request, "You are not registered as a landlord.")
        return redirect('landlord:register')

    rooms = Room.objects.filter(landlord=request.user).order_by('-created_at')

    context = {
        'rooms': rooms,
    }
    return render(request, 'landlord/my_listings.html', context)


# =========================================================
# 6. LOGOUT
# =========================================================

def logout_landlord(request):
    """
    Logs out the landlord and redirects to the login page.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('landlord:login')