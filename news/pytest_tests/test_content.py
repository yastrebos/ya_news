import pytest
from django.urls import reverse
from django.conf import settings
from news.models import News, Comment

HOME_URL = reverse('news:home')


def test_news_count(author_client, news_list):
    News.objects.bulk_create(news_list)
    response = author_client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count, settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(author_client, news_list):
    News.objects.bulk_create(news_list)
    response = author_client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates

# def test_comments_order(author_client, comments_list, id_news_for_args):
#     Comment.objects.bulk_create(comments_list)
#     detail_url = reverse('news:detail', args=id_news_for_args)
#     response = author_client.get(detail_url)
#     # Проверяем, что объект новости находится в словаре контекста
#     # под ожидаемым именем - названием модели.
#     assert 'news' in response.context
#     # Получаем объект новости.
#     news = response.context['news']
#     # Получаем все комментарии к новости.
#     all_comments = news.comment_set.all()
#     # Проверяем, что время создания первого комментария в списке
#     # меньше, чем время создания второго.
#     assert all_comments[0].created < all_comments[1].created
