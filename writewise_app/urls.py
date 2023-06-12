from django.urls import path
from .views import chat
from . import views

urlpatterns = [
    path('api/chat/',views.chat, name='chat'),
    path('api/daily_report/', views.daily_report, name='create_report_daily'),
    path('api/goal_report/', views.goal_report, name='goal_report'),
    path('api/observations_report/', views.observations_report, name='observations_report'),
    path('api/critical_reflection/', views.critical_reflection, name='critical_reflection'),
    path('api/to_do_australia/', views.to_do_australia, name='to_do_australia'),
    path('api/save_report/', views.save_report, name='save_report'),
    path('api/historical_report/', views.historical_report, name='historical_report'),
    path('api/weekly_reflection/', views.weekly_reflection, name='weekly_reflection'),
    path('api/weekly_planning/', views.weekly_planning, name='weekly_planning'),
    path('api/get_historical_report/', views.get_historical_report, name='get_historical_report'),
    path('api/get_variables_reports/', views.get_variables_reports, name='get_variables_reports'),
    path('api/days_to_weekly_reflection/', views.days_to_weekly_reflection, name="days_to_weekly_reflection"),
    path('api/follow_up/',views.follow_up, name='follow_up'),
    path('api/get_last_variable/', views.get_last_variable_report, name='get_last_variable'),
    path('api/create-word/', views.create_word, name='create-word'),
    
    
    
]
