import datetime
from pathlib import Path
from .views import mail_sender
from django.http import HttpResponse
from taskapp.models import *


def my_cron_job():
    import datetime
    report = Reporting.objects.filter(duration_from=datetime.datetime.now().date())
    for data in report:
        person = User.objects.filter(reporting_to=data.existing_reporting_to)
        for name in person:
            name.reporting_to = data.new_reporting_to
            name.save()
    report = Reporting.objects.filter(duration_till=datetime.datetime.now().date())
    for data in report:
        person = User.objects.filter(reporting_to=data.new_reporting_to)
        for name in person:
            name.reporting_to = data.existing_reporting_to
            name.save()


def create_daily_attendence():
    try:
        a = User.objects.all()
        for i in a:
            today = datetime.datetime.now().date()
            print(today)
            if Attendence.objects.filter(user_id=i.id, attend_date=today).exists():
                pass
            else:
                print("attndace")
                Attendence.objects.create(user_id=i.id)
    except Exception as e:
        print(e)


from notification.views import send_notification
from taskapp.models import Store_token, Notification_record


def send():
    resgistration = []
    data = Store_token.objects.all()
    for i in data:
        resgistration.append(i.token)
        x = User.objects.filter(username=i.user).last()
        Notification_record.objects.create(user_id=x.id, status="send")
    send_notification(resgistration, 'Attendance', 'click to punch in attendance')
    return HttpResponse("sent")


def birthday_messages():
    import datetime
    user_list = []
    birthday_data = User.objects.filter(birthday__icontains=datetime.datetime.now().date().strftime('%m-%d'),
                                        is_active=True)
    get_all = User.objects.filter(is_active=True)
    for i in get_all:
        user_list.append(i.email)
    print("today birthday", birthday_data)
    for user_data in birthday_data:
        print("data", user_data)
        print("user", user_data.birthday)
        try:
            path_url = user_data.profile.url
        except:
            path_url = None

        print("ok")
        print("now", datetime.datetime.now().date().strftime('%m-%d'))
        print("db", user_data.birthday.strftime('%m-%d'))
        if user_data.birthday.strftime('%m-%d') == datetime.datetime.now().date().strftime('%m-%d'):
            if path_url:
                path_url = user_data.profile.url
                print(path_url)
                original_path = "/".join(path_url.strip("/").split('/')[0:])
                print(original_path)
                image_path = original_path
                image_name = Path(image_path).name
            else:
                image_path = " "
                image_name = " "
            recipient = [user_data.email]
            print(recipient)
            sender = "bestwishes@visiontrek.in"
            subject = "Happy Birthday!!"
            text_message = f"“Wishing you the best on your birthday and everything good in the year ahead.” “Hope your day is filled with happiness.” “Wishing you a happy birthday and a wonderful year.” “Our whole team is wishing you the happiest of birthdays.” {image_name}."
            username = user_data.username.title()
            html_message = f"""
                <html>
                <style>
                  margin:40,30,40,30;
                </style>
                <body>
                <h2>Happy Birthday {username}!!!</h2>
                   <p class="mk" width="70%"> On behalf of the entire Visiontrek Team,Accordingly, for being the most incredible employee and the most versatile member of our team, your birthday is a big deal for us. Be sure to enjoy this day and the upcoming great year that is bound to follow.<br>
                    </p>
                    <br>
                    <center> <img src='cid:{image_name}' style="object-fit: contain;"/></center>
                    <br><br>
                    <p>Best Wishes,<br>
                    Visiontrek Communication</p>
                </body> 
            </html>
            
                """

            mail_sender(subject=subject, text_content=text_message, html_content=html_message, sender=sender,
                        recipient=recipient, cc=user_list, image_path=image_path, image_name=image_name)
