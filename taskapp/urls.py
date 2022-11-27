from django.urls import path

from taskapp import views

urlpatterns =[
    path('', views.all_tasks),
    path('add-task', views.add_task),
    path('view-task/<str:id>', views.view_single_task),
    path('edit-task/<str:id>', views.edit_task),
    path('task-type/<str:type>', views.task_type),
    path('delete-task/<str:id>', views.delete_task),


    # REPORTING
    path('view-user-reporting-to/', views.contact_user_reporting_to),
    path('view-user-reporting-by/', views.contact_user_reporting_by),
    path('view-user-reporting-by-all-task/<str:user_id>', views.view_reported_by_user_all_task),
    path('view-user-reporting-by-all-project/<str:user_id>', views.view_reported_by_user_all_project),
    path('manage-reporting/', views.manage_reporting),


    # TEAM
    path('view-user-team-member/', views.contact_team_members),


    # ATTENDENCE
    path('mark-attendence/', views.mark_attendence),
    path('mark-attendence-out/', views.mark_attendence_out),
    path('single-user-attendence-detail/', views.single_user_detail_attendence),

    #LEAVE

    path('apply-leave/',views.apply_leave),
    path('user-leave-view/',views.view_leave_detail),




    # path('value/', views.value),
    # path('value1/', views.getting),
    # path('hello/', views.presence_change),

    # path('hello/', views.create_daily_attendence),


    # path('view-chart',views.view_chart),

]
