from datetime import datetime

from django import forms

from taskapp.models import *




class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

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

class TaskUploadedFileForm(forms.ModelForm):
    class Meta:
        model=task_uploaded_file
        exclude =('task', 'uploaded_file', 'extension', )


class ManageReportForm(forms.ModelForm):
    class Meta:
        model= Reporting
        fields=('reported_by','existing_reporting_to','new_reporting_to','duration_from','duration_till')



class AttendenceForm(forms.ModelForm):
    class Meta:
        model=Attendence
        exclude=('attend_date','user')

        def clean_attend_date(self):
            attend_date = self.cleaned_data["attend_date"]
            if Attendence.objects.filter(attend_date=datetime.now().date()).exists():
                raise forms.ValidationError('Cannot Punch In Again!!')
            return attend_date

class LeaveForm(forms.ModelForm):
    class Meta:
        model=Leave
        exclude=('attendence','user','is_pending','is_approved','is_rejected')