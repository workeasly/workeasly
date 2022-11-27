from django.shortcuts import render

# Create your views here.
from projectapp.forms import AddNewProjectForm
from projectapp.models import Project
from taskapp.models import Task, task_uploaded_file
from django.contrib.auth.decorators import login_required

@login_required(login_url="/")
def user_projects(request, project_id=None):
    if project_id=="completed": \
            all_projects = Project.objects.filter(user=request.user,completed=True).order_by('-id')
    elif project_id=="active":
        all_projects = Project.objects.filter(user=request.user,is_active=True).order_by('-id')
    else:
         all_projects=Project.objects.filter(user=request.user).order_by('-id')
    return render(request, "projectapp/user_projects.html", locals())

@login_required(login_url="/")
def add_new_project(request):
    if request.method == "POST":
        form = AddNewProjectForm(request.POST)
        f = form.save(commit=False)
        f.user = request.user
        f.title=request.POST['project_title']
        f.details=request.POST['task_details']
        if request.POST.get('status')=="active":
            f.is_active = True
            f.completed = False
            f.started_on = request.POST['start_date']

            f.save()
            added = True
        elif request.POST.get('status') == "completed":
            f.completed_on = request.POST['completed_date']
            f.completed=True
            f.is_active = False
            f.started_on = request.POST['start_date']

            f.save()
            added = True
        else:
            status_not_selected=True



    return render(request, "projectapp/add_new_project.html", locals())

@login_required(login_url="/")
def update_project(request, project_id):
    project_details = Project.objects.get(id=project_id)
    task_details = Task.objects.filter(user=request.user, project_id=project_id).order_by('-id')
    uploaded_files_data = task_uploaded_file.objects.filter(task__project_id=project_id)
    return render(request, "projectapp/update_project.html", locals())

@login_required(login_url="/")
def project_detail_view(request, project_id):
    if request.method == "POST":
        update_data = Project.objects.get(id=project_id)
        update_data.is_active=False
        update_data.completed=True
        update_data.completed_on=request.POST['completed_date']
        update_data.save()


        form = AddNewProjectForm(request.POST)
    project_details=Project.objects.get(id=project_id)
    task_details=Task.objects.filter(user=request.user,project_id=project_id).order_by('-id')
    uploaded_files_data=task_uploaded_file.objects.filter(task__project_id=project_id)
    return render(request, "projectapp/project_detail_view.html", locals())
