from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ajax/lifetime-aion-stats/', views.ajax_lifetime_aion_stats),
    path('ajax/lifetime-school-stats/', views.ajax_lifetime_school_stats),

]