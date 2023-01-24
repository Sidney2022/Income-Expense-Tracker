from django.contrib import admin

from .models import UserPreferences

class UserPreferencesAdmin(admin.ModelAdmin):
    list_display=('user', 'currency', 'email_subscription', 'sms_notification')

admin.site.register(UserPreferences, UserPreferencesAdmin)
