from django.urls import path

from website import dashboard_views as views

urlpatterns = [
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),
    path('', views.dashboard_home, name='dashboard_home'),
    path('profile/', views.dashboard_profile, name='dashboard_profile'),

    path('news/', views.dashboard_news_list, name='dashboard_news_list'),
    path('news/add/', views.dashboard_news_add, name='dashboard_news_add'),
    path('news/<int:row_id>/edit/', views.dashboard_news_edit, name='dashboard_news_edit'),
    path('news/<int:row_id>/delete/', views.dashboard_news_delete, name='dashboard_news_delete'),

    path('research/', views.dashboard_research_list, name='dashboard_research_list'),
    path('research/add/', views.dashboard_research_add, name='dashboard_research_add'),
    path('research/<int:row_id>/edit/', views.dashboard_research_edit, name='dashboard_research_edit'),
    path('research/<int:row_id>/delete/', views.dashboard_research_delete, name='dashboard_research_delete'),

    path('education/', views.dashboard_education_list, name='dashboard_education_list'),
    path('education/add/', views.dashboard_education_add, name='dashboard_education_add'),
    path('education/<int:row_id>/edit/', views.dashboard_education_edit, name='dashboard_education_edit'),
    path('education/<int:row_id>/delete/', views.dashboard_education_delete, name='dashboard_education_delete'),

    path('publications/', views.dashboard_publications_list, name='dashboard_publications_list'),
    path('publications/add/', views.dashboard_publications_add, name='dashboard_publications_add'),
    path('publications/<int:row_id>/edit/', views.dashboard_publications_edit, name='dashboard_publications_edit'),
    path('publications/<int:row_id>/delete/', views.dashboard_publications_delete, name='dashboard_publications_delete'),

    path('teaching/', views.dashboard_teaching_list, name='dashboard_teaching_list'),
    path('teaching/add/', views.dashboard_teaching_add, name='dashboard_teaching_add'),
    path('teaching/<int:row_id>/edit/', views.dashboard_teaching_edit, name='dashboard_teaching_edit'),
    path('teaching/<int:row_id>/delete/', views.dashboard_teaching_delete, name='dashboard_teaching_delete'),

    path('awards/', views.dashboard_awards_list, name='dashboard_awards_list'),
    path('awards/add/', views.dashboard_awards_add, name='dashboard_awards_add'),
    path('awards/<int:row_id>/edit/', views.dashboard_awards_edit, name='dashboard_awards_edit'),
    path('awards/<int:row_id>/delete/', views.dashboard_awards_delete, name='dashboard_awards_delete'),

    path('service/', views.dashboard_service_list, name='dashboard_service_list'),
    path('service/add/', views.dashboard_service_add, name='dashboard_service_add'),
    path('service/<int:row_id>/edit/', views.dashboard_service_edit, name='dashboard_service_edit'),
    path('service/<int:row_id>/delete/', views.dashboard_service_delete, name='dashboard_service_delete'),

    path('pages/', views.dashboard_pages_list, name='dashboard_pages_list'),
    path('pages/add/', views.dashboard_page_add, name='dashboard_page_add'),
    path('pages/<int:page_id>/edit/', views.dashboard_page_edit, name='dashboard_page_edit'),
    path('pages/<int:page_id>/delete/', views.dashboard_page_delete, name='dashboard_page_delete'),
    path('pages/<int:page_id>/content/', views.dashboard_page_content, name='dashboard_page_content'),
]
