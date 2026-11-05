from django.contrib import admin
from .models import Landlord, LandlordProfile

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    #Admin configuration for the Landlord model
    list_display = ['id', 'user', 'verification_status', 'created_at']
    list_editable = ['verification_status']
    list_filter = ['verification_status']
    readonly_fields = ['created_at', 'updated_at']
    
@admin.register(LandlordProfile)
class LandlordProfileAdmin(admin.ModelAdmin):
    #Admin configuration for the LandlordProfile model
    #This is what the admin will see about the landlord profile
    list_display = ['id', 'user', 'full_name', 'phone_number', 'date_of_birth', 'id_verified_at']
    search_fields = ['full_name', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']