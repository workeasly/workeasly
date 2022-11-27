from django.urls import path

from dashboardapp import views

urlpatterns = [
    path('', views.dashboard_index),
    path('profile', views.profile),
    path('profile_user', views.password_profile),
    # path('view-chart',views.view_chart),
]
