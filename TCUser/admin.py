from django.contrib import admin
from .models import User

admin.site.register([])


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
