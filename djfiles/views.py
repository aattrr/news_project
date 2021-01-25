from _csv import reader
from django.contrib import messages
from django.http import HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from app_users.models import Profile, News, User
from .forms import RegisterForm, ChangeUserForm, UploadFileForm


def load_file(request):
    """Загрузка .csv файла и сохранение в базу заголовка новости, описания и текущего пользователя"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                data_file = form.cleaned_data['file'].read()
                data_str = data_file.decode('utf-8').split('\n')
                csv_reader = reader(data_str, delimiter=",", quotechar='"')
                for row in csv_reader:
                    News.objects.create(title=row[0], description=row[1], user=request.user)
                return HttpResponse(content='Данные обновлены', status=200)
        else:
            form = UploadFileForm()
            context = {
                'form': form
            }
            return render(request, 'djfiles/upload_file.html', context=context)
    return render(request, 'djfiles/upload_file.html')


class UserLoginView(LoginView):
    template_name = 'djfiles/login.html'


def edit_profile(request):
    """Редактирование пользователя"""
    if request.user.is_authenticated:
        profile_data = Profile.objects.get(user=request.user)
        # profile_data = get_object_or_404(Profile, user=request.user)
        if request.method == 'POST':
            form = ChangeUserForm(request.POST, instance=profile_data)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = ChangeUserForm(instance=profile_data)
        return render(request, 'djfiles/edit_profile.html', {"form": form})
    else:
        return render(request, 'djfiles/edit_profile.html')


class UserLogoutView(LogoutView):
    template_name = 'djfiles/logout.html'


class MainPage(TemplateView):
    """Главная страница"""
    template_name = "djfiles/main.html"


class PersonalInf(TemplateView):
    """Страница персональной информации"""
    template_name = "djfiles/personal_inf.html"

    def get_context_data(self, **kwargs):
        """Получаем колличество опубликованных новостей"""
        context = super(PersonalInf, self).get_context_data(**kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            select_user = News.objects.filter(user=current_user)
            context['count_news'] = select_user.count()
        return context


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            town = form.cleaned_data.get('town')
            tel = form.cleaned_data.get('tel')
            first_name = form.cleaned_data.get('first_name')
            second_name = form.cleaned_data.get('second_name')
            about_me = form.cleaned_data.get('about_me')
            avatar = form.cleaned_data.get('avatar')
            Profile.objects.create(
                user=user,
                town=town,
                tel=tel,
                first_name=first_name,
                second_name=second_name,
                about_me=about_me,
                avatar=avatar
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Ошибка Регистрации')
    else:
        form = RegisterForm()
    return render(request, 'djfiles/register.html', {'form': form})


def about(request):
    """Страница О нас"""
    context = {
        'about_text': 'Сайт создан в ознакомительных целях для оценки профессиональных способностей'
    }
    return render(request, 'djfiles/about.html', context=context)


def contact(request):
    """Страница Контакты"""
    context = {
        'contact_text': 'Страница контактов'
    }
    return render(request, 'djfiles/contact.html', context=context)
