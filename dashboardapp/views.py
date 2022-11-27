from datetime import datetime,timedelta

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from taskapp.models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from taskapp.models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url="/")
def dashboard_index(request):
    # print(User.objects.all()[0])
    if not request.user.is_superuser:
        employee_tab = True
        user_tasks_count = Task.objects.filter(user=request.user).count()
        user_project_count = Project.objects.filter(user=request.user).count()
        user_attendence_count = Attendence.objects.filter(user=request.user).count()
        user_pending_leave = Leave.objects.filter(user=request.user, is_pending=True).count()
        user_approved_leave = Leave.objects.filter(user=request.user, is_approved=True).count()
        user_rejected_leave = Leave.objects.filter(user=request.user, is_rejected=True).count()

        # z = datetime.now()
        # current_time = z.strftime("%H:%M:%S")
        # detail_attendence=Detail_attendence.objects.filter(user_id=request.user.id).last()
        # p=detail_attendence.punch_in.strftime("%H:%M:%S")

        # fc=datetime.strptime(current_time, "%H:%M:%S")
        # fp=datetime.strptime(p, "%H:%M:%S")
        # total_work= fc - fp

        # complete_on = fp + timedelta(hours=9)
        # completed_on = complete_on.strftime("%H:%M:%S")
        # c_on = datetime.strptime(completed_on, "%H:%M:%S")
        # remaining=c_on-fc

        # if detail_attendence.attend_date==datetime.now().date():
        #     print("hellog")
        #     punch_out = True
        # else:
        #     print("hif")
        #     punch_in=True



    if request.user.is_superuser:
        super_user_tab = True
        total_users = User.objects.filter(is_active=True).count()
        total_ex_users = User.objects.filter(is_active=False).count()
        total_tasks = TaskType.objects.all().count()
        total_departments = ProgrammingLanguage.objects.all().count()
        total_systems = system_detail.objects.all().count()
        total_user_task = Task.objects.all().count()
        total_user_project = Project.objects.all().count()
        total_pending_leave = Leave.objects.filter(is_pending=True).count()
        total_approved_leave = Leave.objects.filter(is_approved=True).count()
        total_rejected_leave = Leave.objects.filter(is_rejected=True).count()

    return render(request, "dashboardapp/dashboard_home.html", locals())

@login_required(login_url="/")
def profile(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        user_db = User.objects.get(id=request.user.id)
        user_db.display_pic = upload
        user_db.profile_updated = True
        user_db.save()
        # fss = FileSystemStorage()
        # file = fss.save(upload.name, upload)
        # file_url = fss.url(file)
    return render(request, "dashboardapp/profile.html", locals())

@login_required(login_url="/")
def password_profile(request):
    user = User.objects.get(id=request.user.id)
    print(user.id)

    if request.method == "POST":
        password = request.POST["password"]
        print("aditi",password)
        user.set_password(str(password))
        user.save()
        updated = True
        user = User.objects.get(id=request.user.id)
        u = authenticate(username=user.username, password=str(password))
        print(u)
        print(u, "this is u")
        if not u:
            return redirect("/")
        else:
            login(request, u)
            print("hello here")

    return render(request, "dashboardapp/chnge_pwd.html",locals())