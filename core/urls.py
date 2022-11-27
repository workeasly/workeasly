"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from core import settings
from indexapp import views

from notification.views import showFirebaseJS

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('sentry-debug/', trigger_error),
    # path('admin/view-user-performance/<str:id>', views.view_chart),
    path('admin/', admin.site.urls),
    path('', views.index_view),
    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.reset, name='reset'),
    path('password-forgot/', views.password_reset),

    # path('logout',views.logout_view),
    # path('tasks',views.all_tasks),
    # path('add-task',views.add_task),
    # path('view-task/<str:id>',views.view_task),
    # path('edit-task/<str:id>',views.edit_task),
    path('dashboard/', include('dashboardapp.urls')),
    path('tasks/', include('taskapp.urls')),
    path('projects/', include('projectapp.urls')),
    path('admin-dashboard/', include('admindashboard.urls')),
    path('notification/', include('notification.urls')),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('firebase-messaging-sw.js', showFirebaseJS, name="show_firebase_js"),
    path("admission-apply",views.apply_admission,name="appliction for admission")
    # path('view-chart',include('')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
   import debug_toolbar
   urlpatterns += [
       url(r'^__debug__/', include(debug_toolbar.urls)),
   ]
