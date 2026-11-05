from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
 #CLASS 1
class Landlord(models.Model):

    #STATUSES
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    )

    #USER- Linking to Django's built-in User model using a OneToOneField
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='landlord'
    )

    #VERIFICATION STATUS
    verification_status = models.CharField(
        max_length=20, 
        choices=VERIFICATION_STATUS_CHOICES, 
        default='pending'
    )

    #TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.verification_status}"


class LandlordProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='landlord_profile'
    )

    

    # Additional profile fields
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    date_of_birth = models.DateField()

    #File
    id_document_path = models.CharField(max_length=500)

    #Picture
    selfie_photo_path = models.CharField(max_length=500)

    id_verified_at = models.DateTimeField(null=True, blank=True)
    id_verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_landlord_docs'
    )

    rejection_reason = models.TextField(null=True, blank=True)

    #TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.full_name}"