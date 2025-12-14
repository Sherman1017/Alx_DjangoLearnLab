from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Book

# ==============================================================================
# TASK 0: CUSTOM USER ADMIN
# ==============================================================================

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 
                'last_name', 
                'date_of_birth', 
                'profile_photo'
            )
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'first_name', 
                'last_name',
                'password1', 
                'password2',
                'date_of_birth',
                'profile_photo',
                'is_staff', 
                'is_active'
            ),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
admin.site.register(CustomUser, CustomUserAdmin)

# ==============================================================================
# TASK 1: BOOK ADMIN
# ==============================================================================

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'created_by', 'created_at')
    list_filter = ('published_date', 'created_at')
    search_fields = ('title', 'author', 'isbn')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new book
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
