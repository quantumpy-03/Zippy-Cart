from django.contrib import admin
from .models import User, CustomerProfile, VendorProfile, UserAddress, ProductCategory

admin.site.register([CustomerProfile, VendorProfile, UserAddress, ProductCategory])

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined', 'email', 'username', 'role', 'password')
    fieldsets = (
        ('Email', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Make core fields readonly when editing
            return self.readonly_fields + ('email', 'username', 'role')
        return self.readonly_fields
