from django import forms

from django.core.exceptions import ValidationError

from taskapp.models import *
from projectapp.models import *



class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        # fields = '__all__'
        fields=("first_name","last_name","username","email","phone_number","office_user_id","reporting_to","programming_language")


    def clean_programming_language(self):
        programming_language=self.cleaned_data["programming_language"]
        if programming_language=="":
            raise forms.ValidationError("this field is required")

        return programming_language

    def clean_email(self):
        email = self.cleaned_data["email"]
        if "@" not in email and "." not in email and " " in email:
            raise forms.ValidationError("Not an Email Address")
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if first_name.isdigit():
            raise forms.ValidationError("This field cannot contain Digits")
        elif '@' in first_name or '-' in first_name or '|' in first_name or '%' in first_name:
            raise ValidationError("This field must contain only alphabet")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if last_name.isdigit():
            raise forms.ValidationError("This field cannot contain Digits")
        elif '@' in last_name or '-' in last_name or '|' in last_name or '%' in last_name:
            raise ValidationError("This field must contain only alphabet")

        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        pun='''!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~'''
        if phone_number.isalpha():
            raise forms.ValidationError("This field contains digits only")
        elif User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Phone number already exists")

        elif len(phone_number)<10:
            raise ValidationError("this field contain only 10 digit number")

        for i in pun:
            if i in phone_number:
                raise ValidationError(f"number field contain only number not {i}")


        return phone_number

    def clean_office_user_id(self):
        office_user_id=self.cleaned_data["office_user_id"]
        print(office_user_id,"here")
        print(type(len(office_user_id)))
        if office_user_id.isalpha():
            print("working")
            raise forms.ValidationError("This field contains digits only")
        elif User.objects.filter(office_user_id=office_user_id).exists():
            raise forms.ValidationError("Office id is already exit")

        return office_user_id

    def clean_username(self):
        username = self.cleaned_data["username"]
        if  username.isdigit():
            raise forms.ValidationError("This field cannot contain Digits")
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        elif  '@' in username or '-' in username or '|' in username or '%' in username:
            raise ValidationError("This field cannot contain Special Character")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    #
class ProgrammingLanguageForm(forms.ModelForm):

    class Meta:
        model=ProgrammingLanguage
        fields=("language_name",)

    def clean_language_name(self):
        language_name = self.cleaned_data["language_name"]
        if  language_name.isdigit():
            raise forms.ValidationError("This field cannot contain Digits")
        elif ProgrammingLanguage.objects.filter(language_name__icontains=language_name).exists():
            raise forms.ValidationError('Language name already exists.')
        elif '@' in language_name or '-' in language_name or '|' in language_name or '%' in language_name:
            raise ValidationError("This field cannot contain Special Character")
        return language_name

class TaskTypeForm(forms.ModelForm):

     class Meta:
         model= TaskType
         fields=("type_name","programming_language","for_all")

     def clean_type_name(self):
        type_name=self.cleaned_data['type_name']
        print(type_name)
        if type_name.isdigit():
            raise forms.ValidationError("This field can't contain Digits")
        elif TaskType.objects.filter(type_name=type_name).exists():
            raise forms.ValidationError("Task name already exists")
        return type_name




class  SystemDetailForm(forms.ModelForm):
     class Meta:
         model= system_detail
         fields=("system_type","specification","system_service","system_id","added_on")

     def clean_system_id(self):
         system_id = self.cleaned_data.get('system_id')
         if system_detail.objects.filter(system_id=system_id).exists():
             raise forms.ValidationError("System already exists")
         elif '@' in system_id  or '|' in system_id or '%' in system_id:
             raise ValidationError("This field cannot contain Special Character")
         return system_id

     def clean_specification(self):
         specification=self.cleaned_data.get('specification')
         if '@' in specification or '-' in specification or '|' in specification or '%' in specification:
             print('hjj')
             raise ValidationError("This field cannot contain Special Character")
         elif specification.isdigit():
             raise ValidationError("this field can't contain only number")
         return specification

     def clean_system_service(self):
         system_service= self.cleaned_data.get('system_service')
         if '@' in system_service or '-' in system_service or '|' in system_service or '%' in system_service:
             raise ValidationError("This field cannot contain Special Character")

         return system_service

class SystemAssignedDetailForm(forms.ModelForm):
    class Meta:
        model=Assigned_System_Detail
        fields=("system_id","user","assigned_type","assigned_on","returned_on")

    def clean_system_id(self):
        b= self.cleaned_data.get('system_id')
        print(b)
        if b =="":
            raise forms.ValidationError("ok")
        return b

    def clean_user(self):
            a=self.cleaned_data.get('user')
            print(a)
            if Assigned_System_Detail.objects.filter(user_id=a).exists():
                raise forms.ValidationError("System already assign to user")
            return a


class ViewUserTaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=("user","task_type","details")

class ViewUserProjectForm(forms.ModelForm):
    class Meta:
        model= Project
        fields=('user', 'title', 'details', 'is_active', 'completed', 'started', 'started_on', 'completed_on','id')



class EventsForm(forms.ModelForm):
        class Meta:
            model=Events
            fields=('title','description','start_date','end_date')
