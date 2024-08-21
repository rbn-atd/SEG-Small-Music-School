"""Configuration of the admin interface."""
from django.contrib import admin
from lessons.models import User, Request, Term, Invoice

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""
    list_display = [
        'id', 'username', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_superuser', 'is_active',
    ]

@admin.register(Request)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for requests"""
    list_display = [
        'id', 'user', 'availability', 'number_Of_Lessons', 'length', 'interval', 'body', 'status', 'date'
    ]


@admin.register(Term)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for terms"""
    list_display = [
        'id', 'term_number', 'start_date', 'end_date'
    ]
@admin.register(Invoice)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for invoices"""
    list_display = [
        'id', 'request','accepting_admin', 'invoice_number', 'cost', 'paid', 'date'

    ]

admin.site.site_title  = "Music School Management System"
admin.site.site_header = "Music School Management System - Admin"


