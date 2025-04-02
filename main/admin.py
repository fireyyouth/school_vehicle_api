from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'role', 'username', 'is_superuser', 'is_staff')

admin.site.register(User, UserAdmin)