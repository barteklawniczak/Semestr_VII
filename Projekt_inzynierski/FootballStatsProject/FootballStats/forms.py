from django import forms
from django.contrib.auth.models import User
from FootballStats.models import File, ToolsDone


class LoginForm(forms.Form):
    username = forms.CharField(label="Username",
                               required=True)
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput,
                               required=True)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

        def clean_password2(self):
            cd = self.cleaned_data
            if cd["password"] != cd["password2"]:
                raise forms.ValidationError("Passwords don't match.")
            return cd["password2"]


class EditUserForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    next = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'uploaded_path',)

    def clean(self):
        cleaned_data = super(UploadFileForm, self).clean()
        return cleaned_data