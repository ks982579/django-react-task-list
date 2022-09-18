"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy

from helpers import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    # Note, we leave out the 'password' field as we don't want to see hashed password
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            gettext_lazy('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            gettext_lazy('Important dates'),
            {'fields':('last_login',)},
        )
    )
    readonly_fields: list = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

# We define our own 'admin_class' to handle how information is displayed. 
admin.site.register(models.User, UserAdmin)
