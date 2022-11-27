from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter

from .forms import UserCreationForm
from .models import *

admin.site.unregister(Group)


list_display = ("type_name", "is_active", "for_all", "programming_language")

admin.site.register(Events)



admin.site.register(Reporting)
admin.site.register(multiple_select_language)
admin.site.register(task_uploaded_file)
admin.site.register(Project)
admin.site.register(Walk_in_Interviwee)






@admin.action(description='Mark selected as Active')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Mark selected as Non-active')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.action(description='Mark selected available for all')
def make_for_all(modeladmin, request, queryset):
    queryset.update(for_all=True)

@admin.action(description='Remove selected available for all')
def make_for_not_all(modeladmin, request, queryset):
    queryset.update(for_all=False)

# @admin.register(User)
class User_Admin(ImportExportModelAdmin,UserAdmin):
    add_form = UserCreationForm
    # form = UserCreationForm
    list_per_page = 10
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'first_name', 'last_name','username','email','programming_language', 'is_employee', 'password1', 'password2','office_user_id')}
         ),
    )

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_employee','programming_language','office_user_id')}),
    )

    list_display = ("pk","first_name", "last_name","username","office_user_id","programming_language","my_url_field")
    search_fields = ("username__startswith","first_name__startswith","email__startswith",)
    def my_url_field(self, obj):
        # "<a href='http://pre.com{0}'>{0}</a>", obj.url)
            return format_html(f"<a href='/admin/view-user-performance/{obj.id}' target='_blank' class='btn btn-sm btn-info'>VIEW</a>")
    my_url_field.allow_tags = True
    my_url_field.short_description = 'CHART'


admin.site.register(User, User_Admin)


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(ImportExportModelAdmin,admin.ModelAdmin):

    list_display = ("language_name", "is_active")
    list_per_page = 10
    actions = [make_active,make_inactive]

@admin.register(Store_password)
class Store_password_Admin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["user", "password"]


@admin.register(TaskType)
class TaskTypeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("type_name", "is_active","for_all","programming_language")
    list_per_page = 10
    actions = [make_active, make_inactive,make_for_all,make_for_not_all]


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "programming_language":
            kwargs["queryset"] = ProgrammingLanguage.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("user", "task_type","display_programming_language","updated_on",)
    list_filter = (("added_on",DateRangeFilter),"task_type__type_name","user__programming_language",)
    search_fields = ("user__username","user__first_name__startswith","user__email__startswith")
    # raw_id_fields = ("task_type", )
    list_per_page = 10

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "task_type":
            kwargs["queryset"] = TaskType.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def display_programming_language(self, obj):
        programming_language = User.objects.get(username=obj.user.username).programming_language
        return programming_language



    display_programming_language.short_description = "Language"




@admin.register(system_detail)
class system_detail_Admin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("system_id", "system_type","specification","added_on")
    list_filter = (("added_on", DateRangeFilter), "system_type","specification")
    search_fields = ("system_id",)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'system_id', 'system_type', 'specification', 'added_on',)}
         ),
    )
    list_per_page = 10


@admin.register(Assigned_System_Detail)
class Assigned_System_Detail_Admin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("user","system_id", "assigned_type","assigned_on","returned_on")
    list_filter = (("assigned_on", DateRangeFilter),("returned_on", DateRangeFilter), "assigned_type","user")
    search_fields = ("system_id__system_id",)

    list_per_page = 10


@admin.register(Detail_attendence)
class Detail_attendence(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("attendence","user", "punch_in","punch_out","attend_date","working_hours")
    search_fields = ("user__username",)

    list_per_page = 10


@admin.register(Attendence)
class Attendence(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("user","attend_date", "presence")

    search_fields = ("attend_date",)

    list_per_page = 10



admin.site.site_header = "WorkEasly Admin Portal"
admin.site.site_title = "WorkEasly Admin Portal"
admin.site.index_title = "WorkEasly Admin Portal"

def get_app_list(self, request):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    ordering = {

        "Users":1,
        "Tasks":2,
        "Task Types":3,
        "Languages / Departments":4,
        "System Details":5 ,
        "Assigned System Details":6,
        "Attendences":7,
        "Eventss":8,
        "Detail_attendences":9,
        "Reportings":10,
        "Multiple_select_languages":11,
        "Task_uploaded_files":12,
        "Projects":13,





    }
    app_dict = self._build_app_dict(request)
    # a.sort(key=lambda x: b.index(x[0]))
    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])

    return app_list

admin.AdminSite.get_app_list = get_app_list
# admin_site = TaskAppAdminSite()