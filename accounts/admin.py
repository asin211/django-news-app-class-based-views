from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    # when you signup/register what kind of fields you want to display on the signup/register page
    list_display = [
        "email",
        "username",
        "age",
        "is_staff",
    ]
    
    fieldsets =  (
        ('Personal info', {
            'fields': ('email', 'username', 'age', 'password',)
        }),
        ('Group Permissions', {
            'classes': ('wide',),
            'fields': ('groups', )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {
            'fields': ('email', 'age',)
        }),
        ('Group Permissions', {
            'classes': ('wide',),
            'fields': ('groups', )
        }),
    )
    
    

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)