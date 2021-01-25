from django.db import models
from django.urls import reverse
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import User



# class Metatag(models.Model):
#     """ Модель тегов, указываемых для новостей """
#     descriptor = models.CharField(max_length=21, verbose_name='тэги', null=True, blank=True)
#
#     def __str__(self):
#         return self.descriptor


class News(models.Model):
    """ Модель новостей """
    user = models.ForeignKey(User, max_length=100, on_delete=models.CASCADE, null=True, blank=True)
    # metatag = models.ManyToManyField(Metatag, max_length=21, null=True, blank=True)
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='содержание')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='дата редактирования')
    status = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        verbose_name_plural = "News"

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Picture(models.Model):
    """ Модель изображений новости, связанная модель """
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='all_pictures_news')
    image = models.ImageField(upload_to='image')


class Comment(models.Model):
    """ Модель коментариев """
    user = models.ForeignKey(User, max_length=100, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(verbose_name='текст комментария')
    news = models.ForeignKey(News, null=True, on_delete=models.CASCADE, verbose_name='новость', blank=True)

    @property
    def short_description(self):
        return truncatechars(self.text, 15)


class Profile(models.Model):
    """ Расширенная модель пользователя """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, verbose_name='Имя', null=True)
    second_name = models.CharField(max_length=150, verbose_name='Фамилия', null=True)
    about_me = models.TextField(verbose_name='Обо мне')
    avatar = models.ImageField(upload_to='image')
    tel = models.CharField(max_length=12, verbose_name='Телефон', null=True)
    town = models.CharField(max_length=1500, verbose_name='Город', null=True)
    check = models.BooleanField(verbose_name='Верифицирован', default=True)
