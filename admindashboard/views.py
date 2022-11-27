import smtplib
import datetime
from email.mime.image import MIMEImage
import logging
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from taskapp.models import *
from .forms import *

from base64 import b64encode, b64decode

from django.core.exceptions import ValidationError

# def all_users(request):
#     all_users_admin_data=User.objects.filter(is_superuser=True).values()
#     print(all_users_admin_data)
#     return render(request, "admindashboard/view_all_user_admin.html")
# all_employees_data=User.objects.filter(is_superuser=False)
# if layout is None:
#     return render(request,"admindashboard/all_users_table_layout.html",locals())
#
# if layout =="tabular":
#     return render(request,"admindashboard/all_users_table_layout.html",locals())
# if layout =="grid":
#     return render(request,"admindashboard/all_users_grid_layout.html",locals())


logger = logging.getLogger(__name__)


@login_required(login_url="/")
def add_new_user(request):
    data = ProgrammingLanguage.objects.filter(is_active=True)
    for i in data:
        print(i.language_name)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        first_name = request.POST["first_name"]
        user_image = request.FILES["image"]
        last_name = request.POST["last_name"]
        birthday = request.POST["birthday"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        alternate_phone_number = request.POST["phone_number1"]
        office_user_id = request.POST["office_user_id"]
        reporting_to = request.POST["reporting_to"]
        joining_date = request.POST["joining_date"]
        programming_language = request.POST["programming_language"]
        if form.is_valid():
            f1 = form.save()
            f1.first_name = first_name
            f1.profile = user_image
            f1.last_name = last_name
            f1.birthday = birthday
            f1.username = username
            f1.password1 = password1
            f1.password2 = password2
            f1.email = email
            f1.phone_number = phone_number
            f1.Alternate_phone_number = alternate_phone_number
            f1.office_user_id = office_user_id
            f1.reporting_to = reporting_to
            f1.joining_date = joining_date
            f1.is_employee = True
            f1.save()
            user = User.objects.get(office_user_id=office_user_id)
            user_password = Store_password.objects.create(user=user, password=password1)
            subject = 'Your Credentials'
            text_content = 'This is an important message.'
            html_content = render_to_string("admindashboard/user.html",
                                            {
                                                "username": username,
                                                "password1": password1

                                            })
            msg = EmailMultiAlternatives(subject, text_content, "uptask@visiontrek.in", [f1.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            added = True

        else:
            notadd = True
            form = UserCreationForm(request.POST)
            return render(request, "admindashboard/add_new_user.html", locals())

    else:
        form = UserCreationForm()
    return render(request, "admindashboard/add_new_user.html", locals())


###########################################
@login_required(login_url="/")
def view_all_users(request):
    view_user = User.objects.filter(is_active=True)
    data = ProgrammingLanguage.objects.all()
    usertask = Task.objects.all()

    return render(request, "admindashboard/view_all_user.html", locals())


@login_required(login_url="/")
def view_inactive_users(request):
    view_user = User.objects.filter(is_active=False)
    data = ProgrammingLanguage.objects.all()
    usertask = Task.objects.all()

    return render(request, "admindashboard/view_all_inactive_user.html", locals())


@login_required(login_url="/")
def update_user(request, id):
    ProgrammingLanguage_data = ProgrammingLanguage.objects.all()
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.first_name = request.POST["first_name"]
        if request.FILES:
            user.profile = request.FILES["profile"]
        user.last_name = request.POST["last_name"]
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.phone_number = request.POST["phone_number"]
        user.Alternate_phone_number = request.POST["Alternate_phone_number"]
        user.office_user_id = request.POST["office_user_id"]
        user.programming_language_id = request.POST["programming_language"]
        user.reporting_to = request.POST["reporting_to"]
        user.birthday = request.POST["birthday"]
        user.joining_date = request.POST["joining_date"]
        user.save()
        added = True
        return redirect("/admin-dashboard/view-all-users/")
    return render(request, "admindashboard/update_user.html", locals())


from datetime import date


@login_required(login_url="/")
def delete_user(request, id):
    user = User.objects.get(id=id)
    print(user)
    print(user.id)
    user.is_active = False
    user.leaving_date = date.today()
    user.save()
    return redirect("/admin-dashboard/view-all-users/")


@login_required(login_url="/")
def add_programming_language(request):
    if request.method == "POST":
        form = ProgrammingLanguageForm(request.POST)
        language_name = request.POST["language_name"]
        if form.is_valid():
            f = form.save()
            f.language_name = language_name
            f.save()
            added = True

        else:
            notadd = True
    else:

        form = ProgrammingLanguageForm(request.POST)
    return render(request, "admindashboard/add_programming_language.html", locals())


@login_required(login_url="/")
def view_all_programming_language(request):
    view_language = ProgrammingLanguage.objects.all()

    return render(request, "admindashboard/view_all_language.html", locals())


@login_required(login_url="/")
def update_programming_language(request, id):
    language = ProgrammingLanguage.objects.get(id=id)
    if request.method == "POST":
        language.language_name = request.POST["language_name"]
        language.is_active = request.POST["is_active"]

        language.save()

        added = True
        return redirect("/admin-dashboard/view-all-programming-language/")
    return render(request, "admindashboard/update_programming_language.html", locals())


@login_required(login_url="/")
def delete_programming_language(request, id):
    language = ProgrammingLanguage.objects.get(id=id)
    language.delete()
    return redirect("/admin-dashboard/view-all-programming-language/")


@login_required(login_url="/")
def add_new_task_type(request):
    data = ProgrammingLanguage.objects.filter(is_active=True)
    if request.method == 'POST':
        form = TaskTypeForm(request.POST)
        print(form)
        if form.is_valid():
            type_name = request.POST['type_name']
            try:
                for_all = request.POST['for_all']
            except:
                for_all = False

            print(for_all)
            created_task_type = TaskType.objects.create(type_name=type_name, for_all=for_all)
            mul_language = TaskType.objects.filter(for_all=False)
            for i in mul_language:
                i.multiple_language = True
                i.save()
            added = True
        else:
            notadd = True
            form = TaskTypeForm(request.POST)

            return render(request, "admindashboard/add_new_task_type.html", locals())

        print(request.POST.getlist('programming_language'), "request.POST.getlist('programming_language')")
        for d in request.POST.getlist('programming_language'):
            print(d)
            multiple_select_language.objects.create(task_type_id=created_task_type.pk, programming_language_id=d)


    else:
        form = TaskTypeForm(request.POST)
    return render(request, "admindashboard/add_new_task_type.html", locals())


@login_required(login_url="/")
def view_all_tasktype(request):
    view_type = TaskType.objects.all()
    a = multiple_select_language.objects.all()
    return render(request, "admindashboard/view_all_task_type.html", locals())


@login_required(login_url="/")
def update_task_type(request, id):
    ProgrammingLanguage_data = ProgrammingLanguage.objects.all()
    view_type_name = TaskType.objects.get(id=id)
    if request.method == "POST":
        view_type_name.type_name = request.POST["type_name"]
        view_type_name.for_all = request.POST["for_all"]
        view_type_name.is_active = request.POST["is_active"]
        # print(type(request.POST.get('for_all')),request.POST.get('for_all'))
        if request.POST.get('for_all') == "False":
            view_type_name.programming_language_id = request.POST["programming_language"]
        elif request.POST.get('for_all') == "True":
            view_type_name.programming_language_id = request.POST["programming_language"]
        view_type_name.save()
        added = True
        return redirect("/admin-dashboard/view-all-tasktype/")
    return render(request, "admindashboard/update_task_type.html", locals())


@login_required(login_url="/")
def delete_task_type(request, id):
    tasktype = TaskType.objects.get(id=id)
    tasktype.delete()
    return redirect("/admin-dashboard/view-all-tasktype/")


@login_required(login_url="/")
def add_system_details(request):
    if request.method == 'POST':
        form = SystemDetailForm(request.POST)
        # print(form)
        system_type = request.POST["system_type"]
        specification = request.POST["specification"]
        system_service = request.POST["system_service"]
        system_id = request.POST["system_id"]
        added_on = request.POST["added_on"]
        if form.is_valid():
            f = form.save()
            f.system_type = system_type
            f.specification = specification
            f.system_service = system_service
            f.system_id = system_id
            f.added_on = added_on
            f.save()
            added = True

    else:
        form = SystemDetailForm(request.POST)
    return render(request, "admindashboard/add_system_detail.html", locals())


@login_required(login_url="/")
def view_all_system_details(request):
    system_detail_list = []
    systemdetail = system_detail.objects.all()

    for sd in systemdetail:
        data = {
            'system_type': sd.system_type,
            'specification': sd.specification,
            'system_service': sd.system_service,
            'system_id': sd.system_id,
            'added_on': sd.added_on,
            'status': sd.status,

        }
        assigned_system_detail = Assigned_System_Detail.objects.filter(system_id=sd.system_id,
                                                                       returned_on__isnull=True).first()

        if assigned_system_detail:
            data['user'] = assigned_system_detail.user
        else:
            data['user'] = ''

        system_detail_list.append(data)

    return render(request, "admindashboard/view_all_system_detail.html", {'system_detail_list': system_detail_list})


@login_required(login_url="/")
def update_system_details(request, system_id):
    systemdetail = system_detail.objects.get(system_id=system_id)
    print(systemdetail.system_type)
    if request.method == "POST":
        systemdetail.system_type = request.POST["system_type"]
        systemdetail.specification = request.POST["specification"]
        systemdetail.system_service = request.POST["system_service"]
        systemdetail.save()

        added = True
        return redirect("/admin-dashboard/view-all-system-details/")
    return render(request, "admindashboard/update_system_detail.html", locals())


@login_required(login_url="/")
def delete_system_details(request, system_id):
    systemdetail = system_detail.objects.get(system_id=system_id)
    systemdetail.delete()
    return redirect("/admin-dashboard/view-all-system-details/")


@login_required(login_url="/")
def add_new_assigned_system_detail(request):
    user = User.objects.all()
    systemdetail = system_detail.objects.all()
    print(systemdetail)
    for i in systemdetail:
        print(i.system_type)
        print(i.system_id)
    if request.method == "POST":
        print("anju", request.POST["sys_id"])
        get = system_detail.objects.get(system_id=request.POST["sys_id"])
        if get.status == "Free":
            print("yess")
            if not Assigned_System_Detail.objects.filter(user_id=request.POST["user"],
                                                         returned_on__isnull=True).exists():
                x = Assigned_System_Detail.objects.create(system_id_id=request.POST["sys_id"],
                                                          user_id=request.POST["user"],
                                                          assigned_type=request.POST["assigned_type"],
                                                          assigned_on=request.POST["assigned_on"])

                systemdetails = system_detail.objects.get(system_id=request.POST["sys_id"])
                systemdetails.status = "Assigned"
                systemdetails.save()
                added = True
                return render(request, "admindashboard/add_new_assigned_system_detail.html", locals())

            else:
                notaddeduser = True
                return render(request, "admindashboard/add_new_assigned_system_detail.html", locals())

        else:
            print("assigned systsenm")
            notadded = True
            return render(request, "admindashboard/add_new_assigned_system_detail.html", locals())
    else:
        # form =SystemAssignedDetailForm(request.POST)
        return render(request, "admindashboard/add_new_assigned_system_detail.html", locals())


@login_required(login_url="/")
def detail_assign_system(request):
    x = request.GET.get('system')
    y = system_detail.objects.get(system_id=x)
    print(y)
    return render(request, "admindashboard/system.html", locals())


@login_required(login_url="/")
def view_all_assigned_system_detail(request):
    assignedsystem = Assigned_System_Detail.objects.all()
    return render(request, "admindashboard/view_all_assigned_system_detail.html", locals())


@login_required(login_url="/")
def update_assigned_system_details(request, id):
    user = User.objects.all()
    systemdetail = system_detail.objects.all()
    assignedsystem = Assigned_System_Detail.objects.get(id=id)
    print("you", assignedsystem.system_id)
    print("you", assignedsystem.user)
    if request.method == "POST":
        assignedsystem.system_id_id = request.POST["system_id"]
        assignedsystem.user_id = request.POST["user"]
        assignedsystem.assigned_type = request.POST["assigned_type"]
        assignedsystem.returned_on = request.POST["returned_on"]
        if assignedsystem.returned_on is not None:
            print("hettete")
            system_value = system_detail.objects.get(system_id=assignedsystem.system_id)
            print("i", system_value.system_id)
            system_value.status = "Free"
            system_value.save()

        assignedsystem.save()

        added = True
        return redirect("/admin-dashboard/view-all-assigned-system-details/")
    return render(request, "admindashboard/update_assigned_system_detail.html", locals())


@login_required(login_url="/")
def delete_assigned_system_details(request, id):
    assignedsystem = Assigned_System_Detail.objects.get(id=id)
    assignedsystem.delete()
    return redirect("/admin-dashboard/view-all-assigned-system-details/")


@login_required(login_url="/")
def view_all_user_task(request):
    usertask = Task.objects.all()
    return render(request, "admindashboard/view_all_user_task.html", locals())


@login_required(login_url="/")
def view_single_user_task(request, id):
    task = Task.objects.get(id=id)
    uploaded_files_data = task_uploaded_file.objects.filter(task__id=id)
    for i in uploaded_files_data:
        print(i.uploaded_file)

    return render(request, "admindashboard/view_single_user_task.html", locals())


@login_required(login_url="/")
def view_all_user_project(request):
    userproject = Project.objects.all()
    return render(request, "admindashboard/view_all_user_project.html", locals())


@login_required(login_url="/")
def view_single_user_project(request, project_id):
    userproject = Project.objects.get(id=project_id)
    task_details = Task.objects.filter(project_id=project_id).order_by('-id')
    uploaded_files_data = task_uploaded_file.objects.filter(task__project_id=project_id)
    return render(request, "admindashboard/view_single_user_project.html", locals())


@login_required(login_url="/")
def view_user_contact(request):
    user_detail = User.objects.all()
    return render(request, "admindashboard/view_user_contact.html", locals())


@login_required(login_url="/")
def view_single_user_all_task(request, user_id):
    taskdetail = Task.objects.filter(user_id=user_id)
    userdetail = User.objects.filter(id=user_id)
    return render(request, "admindashboard/single_user_all_task.html", locals())


@login_required(login_url="/")
def view_single_user_all_project(request, user_id=None):
    all_projects = Project.objects.filter(user_id=user_id).order_by('-id')
    userdetail = User.objects.filter(id=user_id)
    return render(request, "admindashboard/view_single_user_all_project.html", locals())


@login_required(login_url="/")
def view_all_user_attendance(request):
    view_user = User.objects.all()
    return render(request, "admindashboard/view_all_user_attendence.html", locals())


def view_single_user_attendence(request, user_id):
    get_detail = Detail_attendence.objects.filter(user_id=user_id)
    userdetail = User.objects.filter(id=user_id)
    return render(request, "admindashboard/view_single_user_attendence.html", locals())


def view_today_all_attendence(request):
    today = Attendence.objects.filter(attend_date=datetime.datetime.now().date())
    return render(request, "admindashboard/view_today_all_attendence.html", locals())


@login_required(login_url="/")
def add_events(request):
    print('request::', request.method)
    if request.method == "POST":
        form = EventsForm(request.POST)
        title = request.POST["title"]
        description = request.POST["description"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        date_1 = datetime.strptime(end_date, "%Y-%m-%d")

        add_time = date_1 + timedelta(days=1)
        # add_time=end_date + timedelta(days=1)
       
        if form.is_valid():
            f1 = form.save()
            f1.title = title
            f1.description = description
            f1.start_date = start_date
            f1.end_date = add_time
            f1.save()
            added = True
        else:
            print("hello")
            form = EventsForm(request.POST)
            print(form)
            print("bye")
        print("ok")
        return render(request, "admindashboard/add_events.html", locals())
    else:
        form = EventsForm()
        print(form)
    return render(request, "admindashboard/add_events.html", locals())


@login_required(login_url="/")
def view_events(request):
    event_data = Events.objects.all()
    for i in event_data:
        print(i.title)
        print(i.start_date)
    return render(request, "admindashboard/view_events.html", locals())


@login_required(login_url="/")
def view_all_leave_detail(request):
    user_detail = User.objects.all()
    detail = Leave.objects.filter(is_pending=True)
    for i in detail:
        print(i.leave_type)
    return render(request, "admindashboard/all_leave_detail.html", locals())


@login_required(login_url="/")
def view_pending_leave_detail(request):
    pending_detail = Leave.objects.filter(is_pending=True)
    for i in pending_detail:
        print(i)
        print(i.leave_type)
    return render(request, "admindashboard/pending_leave_detail.html", locals())


@login_required(login_url="/")
def view_approved_leave_detail(request):
    approved_detail = Leave.objects.filter(is_approved=True)
    for i in approved_detail:
        print(i.leave_type)
    return render(request, "admindashboard/approved_leave_detail.html", locals())


@login_required(login_url="/")
def view_rejected_leave_detail(request):
    rejected_detail = Leave.objects.filter(is_rejected=True)
    for i in rejected_detail:
        print(i.leave_type)
    return render(request, "admindashboard/rejected_leave_detail.html", locals())



def mail_sender(subject, text_content, html_content=None, sender=None, cc=None, recipient=None, image_path=None,
                image_name=None):
    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=sender,
                                   to=recipient, bcc=cc if isinstance(recipient, list) else [recipient])
    if all([html_content, image_path, image_name]):
        email.attach_alternative(html_content, "text/html")
        email.content_subtype = 'html'  # set the primary content to be text/html
        email.mixed_subtype = 'related'  # it is an important part that ensures embedding of an image
        with open(image_path, mode='rb') as f:
            image = MIMEImage(f.read())
            email.attach(image)
            image.add_header('Content-ID', f"<{image_name}>")
    email.send()

    return HttpResponse("success")


@login_required(login_url="/")
def send_mail(request, id):
    user = Store_password.objects.get(user_id=id)
    user_detail = User.objects.get(id=user.user_id)

    subject = 'Your Credentials'
    text_content = 'This is an important message.'
    html_content = render_to_string("admindashboard/user_credentials.html",
                                    {
                                        "user": user,
                                        "user_detail": user_detail,

                                    })
    msg = EmailMultiAlternatives(subject, text_content, "uptask@visiontrek.in", [user_detail.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return redirect("/admin-dashboard/view-all-users/")


import requests

import json
from indexapp.models import Admission

@login_required(login_url="/")
def my_django_view(request):
    admission = Admission.objects.all()
    return render(request, "admindashboard/view_interviewee_record.html", locals())


import os


@login_required(login_url="/")
def Add_interviwe_detail(request):
    print("fhgfhghgh")
    if request.method == "POST":
        add_detail = Walk_in_Interviwee.objects.create(name=request.POST["name"],
                                                       interviwer_name=request.POST["interviwer_name"],
                                                       profile=request.POST["profile"],
                                                       experience=request.POST["experience"],
                                                       date=request.POST["date"],
                                                       status=request.POST["status"],
                                                       cv=request.FILES["cv"])
        x = add_detail.cv
        name, extension = os.path.splitext(add_detail.cv.name)
        print(extension == ".pdf")
    return render(request, "admindashboard/add_interviewee_detail.html", locals())



import facebook


@login_required(login_url="/")
def Add_events(request):
    try:
        token = "EAAIvRkNIWtEBADGBOSqgCom43cKgV5MpOVNm2OaPZC0XdayuBBUVuZBK8EDqzRJ6hHSls3spGUFtk1qZBm6h1yTlH6I9VHIioqYXAKBntkMsqGZA9r0QgeZAyOlzdOl7fVWgb8aHopErbLvjKCTrh6IvIRpZCl7ihUsdM17S7V7ivnRRpcAADx"
        graph = facebook.GraphAPI(access_token=token)

        if request.method == "POST":
            photo = request.FILES.getlist("photo")

            add_detail = AddEvent.objects.create(title=request.POST["title"],
                                                 description=request.POST["description"],
                                                 event_date=request.POST["event_date"])

            imgs_id = []
            for i in photo:
                get = Event_photo.objects.create(addevent_id=add_detail.id, photo=i)

                print(get.photo)

                image = f"http://www.uptaskdemo.visiontrek.in{get.photo.url}"
                message = f"{add_detail.title}\n{add_detail.description}"

                id = "109927938447853"
                upload = graph.put_object(id, 'photos', message=message, url=image, published=False)
                print(f"upload:", upload)
                imgs_id.append(upload['id'])
                added = True

            args = dict()
            args["message"] = message

            for img_id in imgs_id:
                key = "attached_media[" + str(imgs_id.index(img_id)) + "]"
                args[key] = "{'media_fbid': '" + img_id + "'}"

            print(f"args", args)
            resp = graph.put_object(
                parent_object="me",
                connection_name="feed",
                **args
            )

            print("resp", resp)

        return render(request, "admindashboard/add_event.html", locals())
    except Exception as ex:
        logger.error(str(ex), exc_info=True)


@login_required(login_url="/")
def Leave_Action(request, action, id):
    if action == "approve":
        get_user_leave = Leave.objects.get(id=id)
        get_user_leave.is_approved = True
        get_user_leave.is_pending = False
        get_user_leave.save()
    elif action == "reject":
        get_user_leave = Leave.objects.get(id=id)
        get_user_leave.is_rejected = True
        get_user_leave.is_pending = False
        get_user_leave.save()
    return redirect("/admin-dashboard/view-all-leave/")


@login_required(login_url="/")
def view_events(request):
    event = AddEvent.objects.all()
    for i in event:
        print(i.title)
        print(i.description)
    return render(request, "admindashboard/view_all_events.html", locals())






########################################################################################################################
