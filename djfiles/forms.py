from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from app_users.models import Profile, News
from django.contrib.auth.forms import UserChangeForm


class RegisterForm(UserCreationForm):
    tel = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={'class': 'mb-0', 'type': 'text', 'placeholder': 'Телефон'}))
    town = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'text', 'placeholder': 'Город'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'text', 'placeholder': 'Имя'}))
    second_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'text', 'placeholder': 'Фамилия'}))
    about_me = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'mb-0', 'type': 'text', 'placeholder': 'Обо мне'}))
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'mb-0', 'type': 'file', 'placeholder': 'Аватар'}))
    password1 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'password', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'password', 'placeholder': 'Подтверждение пароля'}))
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'mb-0', 'type': 'text', 'placeholder': 'Имя пользователя'}))

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'second_name', 'about_me', 'tel', 'town', 'avatar', 'password1', 'password2'
        )


class ChangeUserForm(UserChangeForm):
    
    def __init__(self, *args, **kwargs):
        super(ChangeUserForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'second_name', 'about_me', 'tel', 'town')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'mb-0', 'type': 'text'}),
            'second_name': forms.TextInput(attrs={'class': 'mb-0', 'type': 'text'}),
            'about_me': forms.Textarea(attrs={'class': 'mb-0', 'type': 'text'}),
            'tel': forms.NumberInput(attrs={'class': 'mb-0', 'type': 'text'}),
            'town': forms.TextInput(attrs={'class': 'mb-0', 'type': 'text'}),
        }


class UploadFileForm(forms.Form):
    file = forms.FileField()
