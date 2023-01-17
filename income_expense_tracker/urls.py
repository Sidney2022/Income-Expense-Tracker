
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('dashboard/expenses/', include('expense.urls')),
    path('dashboard/income/', include('income.urls')),
    path('auth/', include('user_authentication.urls')),
    path('account/', include('user_preferences.urls')),
]
