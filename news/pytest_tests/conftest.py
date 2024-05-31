import pytest
from datetime import datetime, timedelta

from django.test.client import Client

import yanews
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор комментария')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Новостной заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def id_for_args(news):
    return (news.id,)


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Комментарий'
    )
    return comment


@pytest.fixture
def list_news():
    today = datetime.today()
    news_list = News.objects.bulk_create(
            News(
                title=f'Новость {index}',
                text='Просто текст',
                date=today - timedelta(days=index)
            ) for index in range(
                yanews.settings.NEWS_COUNT_ON_HOME_PAGE + 1
            )
        )
    return news_list


@pytest.fixture
def form_data(news, author):
    return {
        'news': news,
        'author': author,
        'text': 'Новый комментарий'
    }
