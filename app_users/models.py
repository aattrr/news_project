from django.db import models
from django.urls import reverse
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save


# class Metatag(models.Model):
#     """ Модель тегов, указываемых для новостей """
#     descriptor = models.CharField(max_length=21, verbose_name='тэги', null=True, blank=True)
#
#     def __str__(self):
#         return self.descriptor


class News(models.Model):
    """ Модель новостей """
    user = models.ForeignKey(
        User, max_length=100, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('user')
    )
    # metatag = models.ManyToManyField(Metatag, max_length=21, null=True, blank=True)
    title = models.CharField(max_length=150, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('date created'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('date update'))
    status = models.BooleanField(verbose_name=_('is active'), default=True)

    class Meta:
        verbose_name_plural = _('news')
        verbose_name = _('new')

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Picture(models.Model):
    """ Модель изображений новости, связанная модель """
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='all_pictures_news', verbose_name=_('news'))
    image = models.ImageField(upload_to='image', verbose_name=_('image'))

    class Meta:
        verbose_name_plural = _('pictures')
        verbose_name = _('picture')


class Comment(models.Model):
    """ Модель коментариев """
    user = models.ForeignKey(
        User, max_length=100, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('user')
    )
    text = models.TextField(verbose_name=_('comment text'))
    news = models.ForeignKey(News, null=True, on_delete=models.CASCADE, verbose_name=_('news'), blank=True)

    class Meta:
        verbose_name_plural = _('comments')
        verbose_name = _('comment')

    @property
    def short_description(self):
        return truncatechars(self.text, 15)


class Profile(models.Model):
    """ Расширенная модель пользователя """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, verbose_name=_('first name'), null=True, blank=True)
    second_name = models.CharField(max_length=150, verbose_name=_('second name'), null=True, blank=True)
    about_me = models.TextField(verbose_name=_('about me'), blank=True)
    avatar = models.ImageField(upload_to='image', verbose_name=_('avatar'), blank=True)
    tel = models.CharField(max_length=12, verbose_name=_('phone'), null=True, blank=True)
    check = models.BooleanField(verbose_name=_('verify'), default=True)

    class Meta:
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')


class Promotion (models.Model):
    """ Программа лояльности """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    offer = models.CharField(max_length=500, verbose_name=_('offer'), null=True, blank=True)
    promotion = models.CharField(max_length=500, verbose_name=_('promotion'), null=True, blank=True)
