from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'first_name', 'last_name', 'passport_id', 'phone_number')
    list_display = ('first_name', 'last_name','email', 'passport_id', 'phone_number', 'address')
    empty_value_display = '----'
