from django.contrib import admin
from .models import users

@admin.register(users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'delete_status', 'create_at')
