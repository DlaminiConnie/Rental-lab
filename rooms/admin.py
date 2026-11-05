from django.contrib import admin
from django.utils import timezone
from .models import Room, RoomPhoto


class RoomPhotoInline(admin.TabularInline):
    model = RoomPhoto
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'city', 'price', 'bedrooms', 'status', 'landlord']
    list_filter = ['status', 'city', 'province']
    # list_editable = ['verification_status']
    search_fields = ['address', 'city', 'description']
    readonly_fields = ['created_at', 'updated_at', 'approved_at', 'approved_by']
    inlines = [RoomPhotoInline]

    actions = ['approve_rooms', 'reject_rooms']

    def approve_rooms(self, request, queryset):
        """Approve selected rooms and mark who approved."""
        count = 0
        for room in queryset:
            room.status = 'approved'
            room.approved_at = timezone.now()
            room.approved_by = request.user
            room.save()
            count += 1
        self.message_user(request, f"{count} room(s) approved successfully.")
    approve_rooms.short_description = "Approve selected rooms"

    def reject_rooms(self, request, queryset):
        """Reject selected rooms."""
        count = queryset.update(status='rejected')
        self.message_user(request, f"{count} room(s) rejected.")
    reject_rooms.short_description = "Reject selected rooms"


@admin.register(RoomPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'display_order', 'uploaded_at']
    search_fields = ['room__address']