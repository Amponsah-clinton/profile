from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', RedirectView.as_view(pattern_name='dashboard_login', permanent=False), name='login'),
    path('dashboard/', include('website.dashboard_urls')),
    path('', include('website.urls')),
]
