from _csv import reader
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from app_users.models import Profile, News, Comment, Promotion
from .forms import RegisterForm, ChangeUserForm, UploadFileForm
from django.utils.translation import gettext as _
from django.core.cache import cache


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
            promotion_cache_key = 'promotion:{}'.format(current_user)
            promotion = Promotion.objects.filter(user=current_user)
            cache.get_or_set(promotion_cache_key, promotion, 30*60)

            context['current_user_comment'] = Comment.objects.filter(user=current_user)
            context['current_user_news'] = News.objects.filter(user=current_user)
            context['current_user_promotion'] = Promotion.objects.filter(user=current_user)
        return context


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data.get('email')
            user = form.save()
            tel = form.cleaned_data.get('tel')
            first_name = form.cleaned_data.get('first_name')
            second_name = form.cleaned_data.get('second_name')
            about_me = form.cleaned_data.get('about_me')
            avatar = form.cleaned_data.get('avatar')
            Profile.objects.create(
                user=user,
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
    about_text = _('The site was created for informational purposes to assess professional abilities')
    return render(request, 'djfiles/about.html', context={'about_text': about_text})


def contact(request):
    """Страница Контакты"""
    contact_text = _('Contact page')
    return render(request, 'djfiles/contact.html', context={'contact_text': contact_text})
