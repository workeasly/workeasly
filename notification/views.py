from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from taskapp.models import *
import requests
import json


def send_notification(registration_ids, message_title, message_desc):
    fcm_api = "AAAAmPVuHa0:APA91bFG81PmXDKWu_HSNXqYbsPmJtrE4GxhQdIA3BEWxWgucmQr9H7egbnQwGstHBZh0G99DKcO8mnmhR8lSDxTUxznQYTkSEQSBaaPfN8V9nnLkfhdniKJffpXD4PettPcin2tuocq"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + fcm_api}

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "notification": {
            "body": message_desc,
            "title": message_title,
            "icon": "https://www.uptaskdemo.visiontrek.in/static/images/logo.png",
            "click_action": "https://www.uptaskdemo.visiontrek.in/tasks/mark-attendence/"
            },
        "data": {
            "openURL": "https://www.uptaskdemo.visiontrek.in/tasks/mark-attendence/"
        }
    }
    result = requests.post(url, data=json.dumps(payload), headers=headers)
    print(result.json())

@csrf_exempt
def home(request):
    print("is_mobile",request.user_agent.is_mobile)
    print("family",request.user_agent.device.family )
    print("new_family",request.user_agent.browser.family)
    print("os family",request.user_agent.os.family)
    print("version string",request.user_agent.os.version_string)
    print("broweser version",request.user_agent.browser.version)
    if request.method == "POST":
        fcm = request.POST['fcm']

        if request.user_agent.is_mobile:
            device = request.user_agent.device.family
        else :
            device = request.user_agent.browser.family
        print(f"device:{device}")
        print(f"parivaar:{request.user_agent.os.family}")
        store_token= Store_token.objects.filter(user=request.user,device=device).last()
        if not store_token:
          Store_token.objects.create(user=request.user,token=fcm,device=device,os=request.user_agent.os.family)
        else:
            store_token.token=fcm
            store_token.save()
    return render(request,"notification/index.html",locals())





def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyDiC7mAqj75uugamxNxOpr0OiS_TyMv-4U",' \
           '        authDomain: "pushnotification-4b81e.firebaseapp.com",' \
           '        databaseURL: "https://pushnotification-4b81e-default-rtdb.europe-west1.firebasedatabase.app/",' \
           '        projectId: "pushnotification-4b81e",' \
           '        storageBucket: "pushnotification-4b81e.appspot.com",' \
           '        messagingSenderId: "656952663469",' \
           '        appId: "1:656952663469:web:2d62cd85ff941afbc85524",' \
           '        measurementId: "G-SYFSB3F2K7"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")
