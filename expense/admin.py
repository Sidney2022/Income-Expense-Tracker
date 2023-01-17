from django.contrib import admin

from .models import Expense, Category

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['owner', 'description', 'date',  'category']
    search_fields = ['description', 'category']
    
    

    
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)

