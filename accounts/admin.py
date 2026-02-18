from django.contrib import admin
from .models import Customer, OTP



class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)

class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'expires_at', 'attempts')
    search_fields = ('user__email', 'otp_code')
    list_filter = ('expires_at',)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(OTP, OTPAdmin)
