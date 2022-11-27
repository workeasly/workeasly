from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import uuid
# Create your models here.
from projectapp.models import Project


class ProgrammingLanguage(models.Model):
    language_name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.language_name

    class Meta:
        verbose_name = 'Languages / Department'

def get_upload_path(instance, filename):
    return 'profile_pictures/{0}/{1}'.format(instance.username, filename)

def get_upload_files_path(instance, filename):
    return 'files/{0}/{1}'.format(instance.task.user.username, filename)

def get_upload_display_profile_path(instance, filename):
    return 'display_profile/{0}/{1}'.format(instance.username, filename)

class User(AbstractUser):
    profile=models.ImageField(null=True,blank=True,upload_to=get_upload_display_profile_path)
    phone_number=models.CharField(max_length=10,null=True,blank=True)
    Alternate_phone_number=models.CharField(max_length=10,null=True,blank=True)
    office_user_id=models.CharField(max_length=255,null=True,blank=True)
    reporting_to=models.CharField(max_length=50,null=True,blank=True)
    is_employee=models.BooleanField(default=False)
    profile_updated=models.BooleanField(default=False)
    display_pic=models.ImageField(blank=True,null=True,upload_to=get_upload_path)
    joining_date=models.DateField(blank=True,null=True)
    leaving_date=models.DateField(blank=True,null=True)
    birthday=models.DateField(blank=True,null=True)
    programming_language=models.ForeignKey(ProgrammingLanguage,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.username


class Attendence(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    attend_date=models.DateField(auto_now_add=True)
    presence=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Leave(models.Model):
    attendence = models.ForeignKey(Attendence, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    leave_period=models.CharField(max_length=20)
    leave_time=models.CharField(max_length=20,null=True,blank=True)
    start_date=models.DateField(auto_now_add=False)
    end_date=models.DateField(auto_now_add=False,null=True,blank=True)
    leave_type=models.CharField(max_length=30)
    leave_description=models.CharField(max_length=100,null=True,blank=True)
    is_pending=models.BooleanField(default=True)
    is_approved=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)



class Events(models.Model):
    title=models.CharField(max_length=30,null=True,blank=True)
    description=models.CharField(max_length=30,null=True,blank=True)
    start_date=models.DateField(auto_now_add=False)
    end_date=models.DateField(auto_now_add=False,null=True,blank=True)



class Detail_attendence(models.Model):
    attendence=models.ForeignKey(Attendence,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    punch_in=models.TimeField(null=True,blank=True)
    punch_out=models.TimeField(null=True,blank=True)
    attend_date=models.DateField(auto_now_add=True,null=True,blank=True)
    working_hours=models.CharField(max_length=30,null=True,blank=True)


class Reporting(models.Model):
    reported_by=models.CharField(max_length=30,null=True, blank=True)
    existing_reporting_to=models.CharField(max_length=30)
    new_reporting_to=models.CharField(max_length=30)
    duration_from=models.DateField(auto_now_add=False)
    duration_till=models.DateField(auto_now_add=False, null=True, blank=True)

class TaskType(models.Model):
     type_name=models.CharField(max_length=255)
     is_active=models.BooleanField(default=True)
     for_all=models.BooleanField(default=False)
     multiple_language = models.BooleanField(default=False)
     programming_language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, null=True, blank=True)

     def __str__(self):
         return self.type_name

     class Meta:
         verbose_name = 'Task Type'

class multiple_select_language(models.Model):

    task_type=models.ForeignKey(TaskType,on_delete=models.CASCADE,null=True,blank=True)
    programming_language=models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, null=True, blank=True)


class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    task_type=models.ForeignKey(TaskType,on_delete=models.CASCADE)
    title=models.CharField(max_length=255,default="",null=True,blank=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    details=models.TextField()
    added_on=models.DateTimeField(auto_now=True)
    updated_on=models.DateTimeField(null=True,blank=True)

    class Meta:

        ordering = ['-id']

    class Meta:
        verbose_name = 'Task'

class task_uploaded_file(models.Model):
     task = models.ForeignKey(Task,on_delete=models.CASCADE)
     uploaded_file = models.FileField(upload_to=get_upload_files_path)
     extension = models.CharField(max_length=255)



system_type_choices= [
        ("Computer", 'Computer'),
        ("Laptop", 'Laptop'),
        ("Macbook", 'MacBook'),
    ]

class  system_detail(models.Model):
    # created_on= models.DateTimeField()
    system_type = models.CharField(max_length=255,choices=system_type_choices,)
    specification = models.TextField()
    system_service = models.TextField(null=True,blank=True)
    system_id=models.CharField(max_length=255,primary_key=True)
    added_on=models.DateTimeField()
    status = models.CharField(max_length=50,default="Free")



    def __str__(self):
        return self.system_id

    class Meta:
        verbose_name = 'System Detail'

assigned_type_choices= [
        ("Temporary", 'Temporary'),
        ("Permanent", 'Permanent'),
    ]
class Assigned_System_Detail(models.Model):
    system_id=models.ForeignKey(system_detail,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_type = models.CharField(max_length=255, choices=assigned_type_choices, )
    assigned_on = models.DateField()
    returned_on=models.DateField(null=True,blank=True)

    class Meta:
        verbose_name = 'Assigned System Detail'

class Store_password(models.Model):
    password=models.CharField(max_length=255,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Store Password'



import os
class Walk_in_Interviwee(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    interviwer_name=models.CharField(max_length=255,null=True,blank=True)
    profile=models.CharField(max_length=255,null=True,blank=True)
    experience=models.CharField(max_length=255,null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    status=models.BooleanField(default=False)
    cv=models.FileField(upload_to='cv')

    def __str__(self):
        return self.name

    def __str__(self):
        name, extension = os.path.splitext(self.cv.name)
        return extension




class AddEvent(models.Model):
    title = models.CharField(max_length=25)
    created_at = models.DateField(auto_now=True)
    event_date = models.DateField()
    description = models.TextField(max_length=240)




class Event_photo(models.Model):
    addevent=models.ForeignKey('AddEvent',on_delete=models.CASCADE,null=True,blank=True)
    photo = models.ImageField(upload_to="event_images", null=True, blank=True)
    created_at = models.DateField(auto_now=True)

class Store_token(models.Model):
    user=models.CharField(max_length=255)
    token=models.TextField()
    device=models.CharField(max_length=255,null=True,blank=True)
    os=models.CharField(max_length=255,null=True,blank=True)


class Notification_record(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateField(auto_now=True)
    status=models.CharField(max_length=240)



