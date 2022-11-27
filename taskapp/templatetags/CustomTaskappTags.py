import pytz
from django import template

from taskapp.models import Task
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter
def check_edit_able(value):
    task_details=Task.objects.get(id=value)
    from datetime import datetime, timedelta
    tz = pytz.timezone("Asia/Calcutta")

    if datetime.now(tz).strftime('%Y-%m-%d') != task_details.added_on.strftime('%Y-%m-%d'):
        link = "<span style='display: none;'></span>"
        return mark_safe(link)

    else:
        link =f"<a href='/tasks/edit-task/{task_details.id}' class='btn btn-warning btn-sm text-white'>EDIT</a>"
        return mark_safe(link)

@register.filter
def user_all_task_type(value):
    links_list=list()
    task_details=Task.objects.values_list('task_type__type_name',flat=True).filter(user=value)
    page_link=""
    repeated_link=""
    for link in task_details:
        print(link,type(link))
        if link==repeated_link:
            pass
        else:
            page_link+=f" <li><a href='/tasks/task-type/{link}'> {link} </a></li>"
            repeated_link=link

    return mark_safe(page_link)


@register.filter
def count_task_type(value,arg):


    task_count = Task.objects.filter(user=arg,task_type__type_name=value).count()
    return task_count

@register.filter
def check_type(value):

    return type(value)
@register.filter
def check_file_type(value,arg):
    if value in ['rgb','gif','pbm','pgm','ppm','tiff','rast','xbm',
    'jpeg/jpg','jpeg','jpg','bmp','png','webp','exr']:
        img_link=f"<img src='/media/{arg}' class='col-6'>"
        return mark_safe(img_link)
    else:
        img_link = f"<a href='/media/{arg}' >Download</a>"
        return mark_safe(img_link)


