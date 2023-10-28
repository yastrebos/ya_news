import pytest
from datetime import datetime, timedelta
from news.models import News, Comment
from django.conf import settings

from news.forms import BAD_WORDS


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def id_news_for_args(news):
    return news.id,


@pytest.fixture
def id_comment_for_args(comment):
    return comment.id,

@pytest.fixture
def news_list():
    # Вычисляем текущую дату.
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            # Для каждой новости уменьшаем дату на index дней от today,
            # где index - счётчик цикла.
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    # News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comments_list(news, author):
    today = datetime.today()
    all_comments = [
        Comment(
            news=news,
            author=author,
            text=f'Tекст {index}',
            created=today - timedelta(days=index)
        )
        for index in range(2)
    ]
    return all_comments


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }


@pytest.fixture
def bad_form_data():
    return {
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст',
    }
