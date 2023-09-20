from django.contrib import admin
from user.models import User, Organization

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('-id',)

class OrganizationAdmin(admin.ModelAdmin):
    #list_display = ('id', 'name', 'address', 'city', 'state', 'country', 'zipcode', 'phone', 'email', 'website', 'logo', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-id',)

admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
