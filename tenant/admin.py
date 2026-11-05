from django.contrib import admin
from .models import Tenant, TenantProfile

@admin.register(Tenant)
class TenantsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'phone_number']
    search_fields = ['full_name', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
# Register your models here.

