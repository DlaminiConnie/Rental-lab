from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tenant(models.Model):
    """
    This model connects a Django User (login account) to the Tenant role.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tenant'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class TenantProfile(models.Model):
    """
    This model stores ALL the personal information the tenant provides
    during registration.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tenant_profile'
    )
    
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.email}"