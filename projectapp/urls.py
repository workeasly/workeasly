from django.urls import path

from projectapp import views

urlpatterns = [
    path('', views.user_projects),
    path('project-type/<str:project_id>/', views.user_projects),
    path('add-project', views.add_new_project),
    path('update/<str:project_id>/', views.update_project),
    path('project-details/<str:project_id>', views.project_detail_view),


    # path('view-chart',views.view_chart),

]
