from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Accounts, UserProfile

class AccountAdmin(UserAdmin):
    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    list_filter = ('is_staff', 'is_superadmin', 'is_active')

    # Define fields in fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superadmin', 'groups', 'user_permissions')}),  
        ('Important Dates', {'fields': ('last_login', 'start_date')}), 
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin', 'is_superadmin', 'groups', 'user_permissions'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('start_date', 'last_activity')  
    
    ordering = ('username',)
    
    # User permissions fields
    filter_horizontal = ('groups', 'user_permissions')

# Register models in the admin panel
admin.site.register(Accounts, AccountAdmin)
admin.site.register(UserProfile)
