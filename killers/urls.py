from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('killers/', views.get_all_killers, name='get_all_killers'),
    path('killers/<str:common_name>/', views.get_killer_by_name, name='get_killer_by_name'),
    path('docs/', views.docs_view, name='docs'),
    path('suggest/', views.suggestion_view, name='suggest'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/update/', views.update_status_view, name='update_status'),
]
