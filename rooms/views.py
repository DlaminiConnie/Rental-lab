from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, RoomPhoto

# 1. VIEW: Browse All Approved Rooms

def browse_rooms(request):
    """
    Displays all approved rooms for tenants to browse.
    """
    rooms = Room.objects.filter(status='approved').order_by('-created_at')
    
    context = {
        'rooms': rooms,
    }
    return render(request, 'rooms/browse.html', context)



# 2. VIEW: Room Detail

def room_detail(request, room_id):
    """
    Displays the full details of a specific room.
    """
    room = get_object_or_404(Room, id=room_id)
    
    context = {
        'room': room,
    }
    return render(request, 'rooms/detail.html', context)


# 3. VIEW: Post a Room (Landlord Only)

@login_required
def post_room(request):
    """
    Allows verified landlords to post a new room listing.
    """
    # Check if user is a verified landlord
    if not hasattr(request.user, 'landlord') or request.user.landlord.verification_status != 'verified':
        messages.error(request, "You must be a verified landlord to post rooms.")
        return redirect('landlord:dashboard')
    
    if request.method == 'POST':
        # Get form data
        price = request.POST.get('price')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')
        bedrooms = request.POST.get('bedrooms')
        description = request.POST.get('description')
        availability_date = request.POST.get('availability_date')
        affidavit = request.FILES.get('affidavit')
        
        # Validation
        if not all([price, address, city, province, bedrooms]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'rooms/post.html')
        
        # Create the room
        room = Room.objects.create(
            landlord=request.user,
            price=price,
            address=address,
            city=city,
            province=province,
            postal_code=postal_code,
            bedrooms=bedrooms,
            description=description,
            availability_date=availability_date,
            affidavit_path=affidavit.name if affidavit else '',
            status='pending'
        )
        
        # Handle photo uploads
        photos = request.FILES.getlist('photos')
        for index, photo in enumerate(photos):
            RoomPhoto.objects.create(
                room=room,
                image_path=photo.name,
                display_order=index
            )
        
        messages.success(request, "Your room has been posted successfully! Awaiting admin approval.")
        return redirect('rooms:my_listings')
    
    return render(request, 'rooms/post.html')



# 4. VIEW: My Listings (Landlord Only)


@login_required
def my_listings(request):
    """
    Displays all rooms posted by the logged-in landlord.
    """
    # Check if user is a landlord
    if not hasattr(request.user, 'landlord'):
        messages.error(request, "You are not registered as a landlord.")
        return redirect('landlord:register')
    
    rooms = Room.objects.filter(landlord=request.user).order_by('-created_at')
    
    context = {
        'rooms': rooms,
    }
    return render(request, 'rooms/my_listings.html', context)


# 5. VIEW: Edit Room (Landlord Only)


@login_required
def edit_room(request, room_id):
    """
    Allows a landlord to edit their pending room listing.
    """
    room = get_object_or_404(Room, id=room_id)
    
    # Check if the logged-in user is the owner
    if room.landlord != request.user:
        messages.error(request, "You don't have permission to edit this room.")
        return redirect('rooms:my_listings')
    
    # Only allow editing if room is pending
    if room.status != 'pending':
        messages.error(request, "This room has already been approved and cannot be edited.")
        return redirect('rooms:my_listings')
    
    if request.method == 'POST':
        # Update room fields
        room.price = request.POST.get('price')
        room.address = request.POST.get('address')
        room.city = request.POST.get('city')
        room.province = request.POST.get('province')
        room.postal_code = request.POST.get('postal_code')
        room.bedrooms = request.POST.get('bedrooms')
        room.description = request.POST.get('description')
        room.availability_date = request.POST.get('availability_date')
        
        # Update affidavit if uploaded
        affidavit = request.FILES.get('affidavit')
        if affidavit:
            room.affidavit_path = affidavit.name
        
        room.save()
        messages.success(request, "Room listing updated successfully! It will need to be re-approved.")
        return redirect('rooms:my_listings')
    
    context = {
        'room': room,
    }
    return render(request, 'rooms/edit.html', context)



# 6. VIEW: Delete Room (Landlord Only)


@login_required
def delete_room(request, room_id):
    """
    Allows a landlord to delete their room listing.
    """
    room = get_object_or_404(Room, id=room_id)
    
    # Check if the logged-in user is the owner
    if room.landlord != request.user:
        messages.error(request, "You don't have permission to delete this room.")
        return redirect('rooms:my_listings')
    
    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted successfully.")
        return redirect('rooms:my_listings')
    
    context = {
        'room': room,
    }
    return render(request, 'rooms/confirm_delete.html', context)

def browse_rooms(request):
    """Displays only approved rooms to tenants."""
    rooms = Room.objects.filter(status='approved').order_by('-created_at')
    context = {
        'rooms': rooms,
    }
    return render(request, 'rooms/browse.html', context)