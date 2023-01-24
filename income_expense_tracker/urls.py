
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('dashboard/expenses/', include('expense.urls')),
    path('dashboard/income/', include('income.urls')),
    path('auth/', include('user_authentication.urls')),
    path('account/', include('user_preferences.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler404='core.views.error_404'