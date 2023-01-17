from django.contrib import admin

from .models import Source, UserIncome

class UserIncomeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'amount', 'source', 'description', 'date',)


admin.site.register(UserIncome, UserIncomeAdmin)
admin.site.register(Source)