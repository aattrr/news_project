from django.urls import path
from .views import *


urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    # path('<int:pk>/news_filter/', NewsFilter.as_view(), name='news_filter'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('add_news/',  create_news, name='add_news'),
    path('<int:pk>/add_comment/', CreateComment.as_view(), name='add_comment'),
    path('<int:pk>/edit_news/', edit_news, name='edit_news'),
    path('<int:pk>/edit_news/delete_picture/', delete_picture, name='delete_picture'),
]
