from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    ROOM_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('inactive', 'Inactive'),
    )

    landlord = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    bedrooms = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    availability_date = models.DateField(blank=True, null=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=ROOM_STATUS_CHOICES,
        default='pending'   # ← New rooms are pending by default
    )


    affidavit_path = models.CharField(max_length=500)

    # Admin tracking fields
    admin_notes = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='approved_rooms'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address} - {self.city} (R{self.price})"


class RoomPhoto(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image_path = models.CharField(max_length=500)
    caption = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.room.address} ({self.display_order})"