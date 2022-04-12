from django.contrib import admin
from django.forms import Textarea

from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class AdminUser(UserAdmin):
    model = User
    ordering = ('-date_joined',)
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    search_fields = ('last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('logo','email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('sex', 'birth_date', 'bio', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2',)
        }),
    )


admin.site.register(User, AdminUser)
