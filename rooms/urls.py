from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    # Public URLs (anyone can view)
    path('', views.browse_rooms, name='browse'),
    path('<int:room_id>/', views.room_detail, name='detail'),
    
    # Landlord-only URLs
    path('post/', views.post_room, name='post'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('<int:room_id>/edit/', views.edit_room, name='edit'),
    path('<int:room_id>/delete/', views.delete_room, name='delete'),
]