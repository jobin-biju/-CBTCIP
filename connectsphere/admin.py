from django.contrib import admin
from .models import registration

@admin.register(registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'address', 'bio')  # Customize the fields you want to display
    search_fields = ('username', 'email')  # Enable search by username or email
    list_filter = ('email',)  # You can filter by email or other fields if needed
