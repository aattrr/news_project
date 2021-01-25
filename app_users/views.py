from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from app_users.models import News, Comment, User, Profile, Picture
from .forms import CommentForm, NewsForm, PictureForm


class NewsList(ListView):
    """ Вывод списка новостей """
    model = News

    def get_context_data(self, **kwargs):
        """Переопределение метода get_context_data для сортировки по созданию активных объявлений"""
        context = super(NewsList, self).get_context_data(**kwargs)
        context['object_list'] = News.objects.filter(status=True).order_by('-create_at')
        # context['cloud_tags'] = Metatag.objects.all
        return context


# class NewsFilter(ListView):
#     """Фильтрация новостей по тегу"""
#     model = News
#     template_name = 'app_users/filter_news.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(NewsFilter, self).get_context_data(**kwargs)
#         select_tag = Metatag.objects.get(id=self.kwargs['pk'])  # Выбраннный тег
#         context['filtered_news'] = News.objects.filter(metatag=select_tag).order_by('-create_at')   # Новости выбранного тега
#         context['select_tag'] = select_tag
#         return context


class NewsDetail(DetailView):
    """Вывод страницы детального описания новости"""
    model = News

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        select_news = News.objects.get(id=self.kwargs['pk'])        # Выбранная новость
        select_picture = Picture.objects.filter(news=select_news)       # Все картинки одной новости
        context['comment_list'] = Comment.objects.filter(news=select_news)
        context['picture_news'] = select_picture
        return context


def create_news(request):
    # if not request.user.has_perm('app_users.add_news'):     # имеет ли пользователь, разрешение на создание новости
    #     raise PermissionDenied()
    if request.user.is_authenticated:
        if request.method == 'POST':
            picture_form = PictureForm(request.POST, request.FILES)
            news_form = NewsForm(request.POST)
            if picture_form.is_valid() and news_form.is_valid():
                news_f = news_form.save(commit=False)
                news_f.user = request.user      # Сохраняем текущего пользователя
                news_f.save()
                news_id = news_f.id     # Получаем id вновь созданной новости
                news = News.objects.get(id=news_id)
                files = request.FILES.getlist('image')  # Получаем все загруженные файлы
                for f in files:
                    instance = Picture(news=news, image=f)
                    instance.save()
                return redirect('news_detail', news_id)
        else:
            context = {
                'news_form': NewsForm(),
                'picture_form': PictureForm(),
            }
            return render(request, 'app_users/add_news.html', context)
    return render(request, 'app_users/add_news.html')

def edit_news(request, pk):
    """Редактирование Новости"""
    if request.user.is_authenticated:
        news_data = News.objects.get(pk=pk)  # Изменяемая новость
        picture_data = Picture.objects.filter(news=news_data)  # И все её картинки
        if request.method == 'POST':
            news_form = NewsForm(request.POST, instance=news_data)
            if news_form.is_valid():
                news_form.save()
                return redirect('news_detail', pk)
        else:
            context = {
                'news_form': NewsForm(instance=news_data),
                'object': picture_data,
                'pk': pk
            }
        return render(request, 'app_users/edit_news.html', context)
    return render(request, 'app_users/edit_news.html')

def delete_picture(request, pk):
    """Удаление картинок из редактируемой новости"""
    # Получаем из checkboxa список id-шников выбранных к удалению картинок
    if request.method == 'POST':
        picture_form = request.POST.getlist('checks')
        if picture_form:
            for pic in picture_form:
                select_picture = Picture.objects.get(id=pic)
                select_picture.delete()
            return redirect('edit_news', pk)
        else:
            return redirect('edit_news', pk)


class CreateComment(CreateView):
    """Создание комментария"""
    form_class = CommentForm
    template_name = 'app_users/add_comment.html'

    def form_valid(self, form):
        user = self.request.user
        news = News.objects.get(id=self.kwargs['pk'])
        if user.is_authenticated:
            new_comment = form.save(commit=False)
            new_comment.news = news
            new_comment.user = user
            new_comment.save()
            return redirect('news_detail', self.kwargs['pk'])
        else:
            new_comment = form.save(commit=False)
            new_comment.news = news
            new_comment.save()
            return redirect('news_detail', self.kwargs['pk'])
