from django.contrib import admin
from user.models import User, Organization


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'is_active', 'role', 'organization', 'first_name', 'last_name',
        'last_login', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'role', 'organization', 'last_login', 'date_joined')
    ordering = ('-id',)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    ordering = ('-id',)


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)

