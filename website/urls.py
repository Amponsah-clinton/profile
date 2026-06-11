from django.urls import path

from website import views

urlpatterns = [
    path('', views.site_page_root, name='site_home'),
    path('<slug>/', views.site_page, name='site_page'),
]
