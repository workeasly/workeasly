from django.urls import path

from notification import views

urlpatterns = [
    path('', views.home),
    path('firebase-messaging-sw.js', views.showFirebaseJS, name="show_firebase_js"),
    path('init-firebase.js', views.showFirebaseJS, name="show_firebase_js"),

]