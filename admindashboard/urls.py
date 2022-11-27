from django.urls import path

from admindashboard import views

urlpatterns = [

    # USER
    # path('all-users/', views.all_users),
    # path('view-all-users-admin/', views.all_users),
    # path('all-users/<str:layout>/', views.all_users),
    path('user-create/', views.add_new_user),
    path('view-all-users/', views.view_all_users),
    path('view-all-inactive-users/', views.view_inactive_users),
    path('edit-user/<str:id>/', views.update_user),
    path('send_credentials/<str:id>/', views.send_mail),
    path('delete-user/<str:id>/', views.delete_user),
    path('add_interviewee_detail/', views.Add_interviwe_detail),
    path('add_event/', views.Add_events),
    path("<str:action>/<str:id>/", views.Leave_Action),

    # path('view-single-user/<str:id>/', views.view_single_user),

    # PROGRAMMING LANGUAGE
    path('create-language/', views.add_programming_language),
    path('view-all-programming-language/', views.view_all_programming_language),
    path('edit-programming-language/<str:id>/',views.update_programming_language),
    path('delete-programming-language/<str:id>/', views.delete_programming_language),

    # TASK
    path('create-tasktype/',views.add_new_task_type),
    path('view-all-tasktype/',views.view_all_tasktype),
    path('edit-task-type/<str:id>/',views.update_task_type),
    path('delete-task-type/<str:id>/',views.delete_task_type),
    path('dummy_api/',views.my_django_view),

    # SYSTEM DETAIL
    path('create-system-details/', views.add_system_details),
    path('view-all-system-details/', views.view_all_system_details),
    path('edit-system-details/<str:system_id>/', views.update_system_details),
    path('delete-system-details/<str:system_id>', views.delete_system_details),
    # path('view-single-system-details/<str:pk>/', views.view_single_system_details),

    # ASSIGNED SYSTEM DETAIL
    path('create-assigned-system-details/', views.add_new_assigned_system_detail),
    path('view-all-assigned-system-details/', views.view_all_assigned_system_detail),
    # path('view-single-assigned-system-details/<str:id>', views.view_single_assigned_system_detail),
    path('edit-assigned-system-details/<str:id>/', views.update_assigned_system_details),
    path('delete-assigned-system-details/<str:id>/', views.delete_assigned_system_details),
    path('get-system', views.detail_assign_system, name="get-system"),
    # path('mail', views.birthday_messages, name="mail"),

    #ALL USER TASK
     path('view-all-user-task/', views.view_all_user_task),
     path('view-single-user-task/<str:id>', views.view_single_user_task),
     path('view-single-user-all-task/<str:user_id>', views.view_single_user_all_task),

    # ALL USER PROJECT
    path('view-all-user-project/', views.view_all_user_project),
    path('view-single-user-project/<str:project_id>', views.view_single_user_project),
    path('view-single-user-all-project/<str:user_id>',views.view_single_user_all_project),

    #VIEW CONTACT
    path('view-user-contact/', views.view_user_contact),
    # path('view/', views.abc),

    # VIEW ATTENDANCE
    path('view-all-user-attendance/', views.view_all_user_attendance),
    path('view-single-user-attendance/<str:user_id>', views.view_single_user_attendence),
    # path('view-chart',views.view_chart),
    path('view-today-all-attendence/', views.view_today_all_attendence),

    path('add-events/', views.add_events),
    path('view-events/', views.view_events),


    path('view-all-leave/', views.view_all_leave_detail),
    path('view-pending-leave/', views.view_pending_leave_detail),
    path('view-approved-leave/', views.view_approved_leave_detail),
    path('view-rejected-leave/', views.view_rejected_leave_detail),





]

