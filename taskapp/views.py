from datetime import timedelta

import pytz
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
# from taskapp.forms import LoginForm
from taskapp.forms import ManageReportForm, AttendenceForm, LeaveForm
from taskapp.models import *


@login_required(login_url="/")
def all_tasks(request):
    all_task_details = Task.objects.select_related().filter(user=request.user).order_by('-id')
    return render(request, "taskapp/all_tasks.html", {'all_task_details': all_task_details})


@login_required(login_url="/")
def view_single_task(request, id):
    all_task_details = Task.objects.get(id=id)
    uploaded_files_data = task_uploaded_file.objects.filter(task__id=id)
    for i in uploaded_files_data:
        print(i.uploaded_file)

    # return render(request, "taskapp/view_single_task.html", {'all_task_details': all_task_details})
    return render(request, "taskapp/view_single_task.html", locals())
    # return HttpResponse("hello")


def task_type(request, type):
    all_task_details = Task.objects.select_related().filter(user=request.user, task_type__type_name=type).order_by(
        '-id')
    return render(request, "taskapp/task_type.html", {'all_task_details': all_task_details, 'requested_type': type})


@login_required(login_url="/")
def add_task(request):
    # alert=True
    all_projects = Project.objects.filter(user=request.user)
    if not all_projects:
        no_projects = True
    all_tasks_type = TaskType.objects.filter(
        Q(is_active=True) & (Q(for_all=True) | (Q(multiple_language=True)) | Q(
            programming_language=request.user.programming_language)))
    if request.method == "POST":
        selected_task_type = request.POST.get('selected_task_type')
        task_details = request.POST.get('task_details')
        tz = pytz.timezone("Asia/Calcutta")
        details_empty = False
        if task_details is None or task_details == "" or task_details == " ":
            details_empty = True
        if not details_empty:
            project = None
            if request.POST['project_selected'] == "1":
                if (request.POST.get('selected_project_type') is not None) or (
                        request.POST.get('selected_project_type') != '') \
                        or (request.POST.get('selected_project_type') != ' '):
                    project = request.POST.get('selected_project_type')
                else:
                    project_not_selected = True
            created_task = Task.objects.create(user=request.user, task_type_id=selected_task_type, details=task_details,
                                               project_id=project,
                                               added_on=datetime.now(tz))

            # form = TaskUploadedFileForm(request.POST, request.FILES)
            # if form.is_valid():
            #     name = form.cleaned_data
            print(request.FILES.getlist('file'), "request.FILES.getlist('file')")
            for f in request.FILES.getlist('file'):
                first_name, last_name = str(f).split('.')
                task_uploaded_file.objects.create(task_id=created_task.pk, uploaded_file=f, extension=last_name)

            added = True
    return render(request, "taskapp/add_task.html", locals())


@login_required(login_url="/")
def view_task(request, id):
    try:
        all_task_details = Task.objects.get(id=id, user=request.user)


    except:
        return redirect("/tasks")
    return render(request, "view_task.html", locals())


@login_required(login_url="/")
def edit_task(request, id):
    try:
        all_task_details = Task.objects.get(id=id, user=request.user)
    except:
        return redirect("/tasks")
    all_tasks_type = TaskType.objects.filter(is_active=True)
    tz = pytz.timezone("Asia/Calcutta")
    if (datetime.now(tz) - all_task_details.added_on) > timedelta(1):
        return redirect("/tasks")
    else:
        if request.method == "POST":
            selected_task_type = request.POST.get('selected_task_type')
            task_details = request.POST.get('task_details')
            tz = pytz.timezone("Asia/Calcutta")
            details_empty = False
            if task_details is None or task_details == "" or task_details == " ":
                details_empty = True
            if not details_empty:
                all_task_details.task_type_id = selected_task_type
                all_task_details.details = task_details
                all_task_details.updated_on = datetime.now(tz)
                all_task_details.save()
                # Task.objects.create(user=request.user,task_type_id=selected_task_type,details=task_details,added_on=datetime.now(tz))
                added = True
                all_task_details = Task.objects.get(id=id)
        return render(request, "taskapp/edit_task.html", locals())


from datetime import datetime


@login_required(login_url="/")
def view_chart(request, id):
    user = User.objects.get(id=id)
    all_tasks = Task.objects.filter(user=id)
    taskapp_dict = dict()
    for task in all_tasks:
        taskapp_dict[task.task_type.type_name] = Task.objects.filter(user=id, task_type=task.task_type).count()

    if 'custom_range' in request.POST:
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')

        date__range = ["2011-01-01", "2011-01-31"]
        for task in all_tasks:
            taskapp_dict[task.task_type.type_name] = Task.objects.filter(user=id, task_type=task.task_type,
                                                                         added_on__gte=from_date,
                                                                         added_on__lte=to_date).count()
    for values in taskapp_dict.values():
        if values == 0 or values == "0":
            empty = True

    if not taskapp_dict:
        empty = True
    return render(request, "view_chart.html", locals())


@login_required(login_url="/")
def manage_reporting(request):
    data = User.objects.filter(programming_language_id=request.user.programming_language)
    reporting_by_user = User.objects.filter(reporting_to=request.user)
    if request.method == 'POST':
        form = ManageReportForm(request.POST)
        new_reporting_to = request.POST['new_reporting_to']
        existing_reporting_to = request.POST['existing_reporting_to']
        duration_from = request.POST['duration_from']
        duration_till = request.POST['duration_till']
        print(request.POST.getlist('reported_by'), "request.POST.getlist('reported_by')")
        for d in request.POST.getlist('reported_by'):
            print(d)
            Reporting.objects.create(reported_by=d, new_reporting_to=new_reporting_to,
                                     existing_reporting_to=existing_reporting_to,
                                     duration_from=duration_from, duration_till=duration_till)
        added = True
    else:
        form = ManageReportForm(request.POST)
    return render(request, "taskapp/manage_reporting.html", locals())


@login_required(login_url="/")
def contact_user_reporting_to(request):
    reporting_to_user = User.objects.get(username=request.user.reporting_to)
    print("anju", reporting_to_user)
    return render(request, "taskapp/view_user_reporting_to_contact_detail.html", locals())


@login_required(login_url="/")
def contact_user_reporting_by(request):
    reporting_by_user = User.objects.filter(reporting_to=request.user)
    return render(request, "taskapp/view_user_reporting_by_contact_detail.html", locals())


@login_required(login_url="/")
def view_reported_by_user_all_task(request, user_id):
    taskdetail = Task.objects.filter(user_id=user_id)
    userdetail = User.objects.filter(id=user_id)
    return render(request, "taskapp/view_reported_by_user_all_task.html", locals())


@login_required(login_url="/")
def view_reported_by_user_all_project(request, user_id=None):
    all_projects = Project.objects.filter(user_id=user_id).order_by('-id')
    userdetail = User.objects.filter(id=user_id)
    return render(request, "taskapp/view_reported_by_user_all_project.html", locals())


@login_required(login_url="/")
def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect("/tasks/")


@login_required(login_url="/")
def contact_team_members(request):
    team_member = User.objects.filter(programming_language_id=request.user.programming_language)
    return render(request, "taskapp/view_user_team_member_detail.html", locals())


@login_required(login_url="/")
def mark_attendence(request):
    # if request.method == 'POST':
    #     form = AttendenceForm(request.POST)
    #     attend_date=request.POST["attend_date"]

    if Attendence.objects.filter(user=request.user, attend_date=datetime.now().date()).exists():
        if not Detail_attendence.objects.filter(user=request.user, attend_date=datetime.now().date()).exists():
            get_key = Attendence.objects.filter(user=request.user, attend_date=datetime.now().date()).last()
            value = get_key.pk
            Detail_attendence.objects.create(user=request.user, punch_in=datetime.now().time(), attendence_id=value)
            a = Attendence.objects.filter(user=request.user, attend_date=datetime.now().date())
            for i in a:
                i.presence = True
                i.save()

            added = True
        return redirect("/tasks/single-user-attendence-detail/")
    return redirect("/tasks/single-user-attendence-detail/")



# else:
#     form = AttendenceForm(request.POST)
# return render(request, "taskapp/mark_attendence.html", locals())


@login_required(login_url="/")
def mark_attendence_out(request):
    a = Detail_attendence.objects.filter(user=request.user, attend_date=datetime.now().date())
    # if request.method == 'POST':
    #     form = AttendenceForm(request.POST)
    #     attend_date = request.POST["attend_date"]
    if Detail_attendence.objects.filter(user=request.user, attend_date=datetime.now().date()).exists():
        Detail_attendence.objects.filter(user=request.user, attend_date=datetime.now().date()).update(
            punch_out=datetime.now().time())
        added = True
    attending = Detail_attendence.objects.filter(user=request.user, attend_date=datetime.now().date())

    for i in attending:
        inn = i.punch_in.strftime("%H:%M:%S")
        print(inn)
        out = i.punch_out.strftime("%H:%M:%S")
        print(out)
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(out, FMT) - datetime.strptime(inn, FMT)
        print(tdelta)
        i.working_hours = tdelta
        print(i.working_hours)
        print("helo")
        i.save()

    return redirect("/tasks/single-user-attendence-detail/")
    # return render(request, "taskapp/mark_punchout_attendence.html", locals())


@login_required(login_url="/")
def single_user_detail_attendence(request):
    detail = Detail_attendence.objects.filter(user=request.user).order_by('-attend_date')
    for i in detail:
        print(i.attendence.presence)
    return render(request, "taskapp/single_user_detail_attendence.html", locals())


#

# def create_daily_attendence(request):
#         a = User.objects.all()
#         for i in a:
#             print(i.id)
#             Attendence.objects.create(user_id=i.id)
#         return HttpResponse("HELO")


@login_required(login_url="/")
def apply_leave(request):
    print('request::', request.method)
    if request.method == "POST":
        form = LeaveForm(request.POST)
        print(form)
        leave_period = request.POST["leave_period"]
        print(leave_period)
        leave_time = request.POST.get("leave_time")
        print(leave_time)
        start_date = request.POST["start_date"]
        print(start_date)
        end_date = request.POST["end_date"]
        print(end_date)
        # date_1 = datetime.strptime(end_date, "%Y-%m-%d")
        # add_time = date_1 + timedelta(days=1)
        # print(add_time)
        leave_type = request.POST["leave_type"]
        print(leave_type)
        leave_description = request.POST["leave_description"]
        print(leave_description)

        if form.is_valid():
            f1 = form.save()
            f1.user = request.user

            f1.leave_time = leave_time
            f1.start_date = start_date
            if leave_type == "full":
                f1.end_date = end_date
            else:
                f1.leave_period = leave_period
                f1.leave_period = leave_period
            f1.leave_type = leave_type
            f1.leave_description = leave_description
            f1.save()
            added = True
        else:
            print("hello")
            form = LeaveForm(request.POST)
            print(form)
            print("bye")
        print("ok")
        return render(request, "taskapp/apply_leave.html", locals())
    else:
        form = LeaveForm()
        print(form)
    return render(request, "taskapp/apply_leave.html", locals())


@login_required(login_url="/")
def view_leave_detail(request):
    leave_detail = Leave.objects.filter(user=request.user)
    for i in leave_detail:
        print(i)
        print(i.leave_type)
    return render(request, "taskapp/user_leave_detail.html", locals())
