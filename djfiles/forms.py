from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from app_users.models import Profile, News
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _



class RegisterForm(UserCreationForm):
    tel = forms.CharField(label=_('Phone'), required=False, widget=forms.NumberInput(
        attrs={'class': 'mb-0', 'type': 'text'}))
    first_name = forms.CharField(label=_('First name'), required=False, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'text'}))
    second_name = forms.CharField(label=_('Second name'), required=False, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'text'}))
    about_me = forms.CharField(label=_('About me'), required=False, widget=forms.Textarea(
        attrs={'class': 'mb-0', 'type': 'text'}))
    avatar = forms.ImageField(label=_('Avatar'), required=False, widget=forms.FileInput(
        attrs={'class': 'mb-0', 'type': 'file'}))
    password1 = forms.CharField(label=_('Password'), required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'password'}))
    password2 = forms.CharField(label=_('Confirm password'), required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'password'}))
    username = forms.CharField(label=_('Username'), required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'text'}))
    email = forms.CharField(label=_('Email'), required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'text'}))

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'second_name', 'about_me', 'tel', 'avatar', 'password1', 'password2', 'email'
        )

    # def save(self, commit=True):
    #         user = super(RegisterForm, self).save(commit=False)
    #         # first_name, last_name = self.cleaned_data["fullname"].split()
    #         # user.first_name = first_name
    #         # user.last_name = last_name
    #         # user.tel = self.cleaned_data["tel"]
    #         # user.email = self.cleaned_data["email"]
    #         # user.first_name = self.cleaned_data["first_name"]
    #         # user.second_name = self.cleaned_data["second_name"]
    #         # user.about_me = self.cleaned_data["about_me"]
    #         # user.avatar = self.cleaned_data["avatar"]
    #         # user.username = self.cleaned_data["username"]
    #         if commit:
    #             user.save()
    #         return user


class ChangeUserForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangeUserForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'second_name', 'about_me', 'tel')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'mb-0', 'type': 'text'}),
            'second_name': forms.TextInput(attrs={'class': 'mb-0', 'type': 'text'}),
            'about_me': forms.Textarea(attrs={'class': 'mb-0', 'type': 'text'}),
            'tel': forms.NumberInput(attrs={'class': 'mb-0', 'type': 'text'}),
            # 'email': forms.TextInput(attrs={'class': 'mb-0', 'type': 'text'}),
        }


class UploadFileForm(forms.Form):
    file = forms.FileField()
