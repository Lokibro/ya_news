import unittest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from news.models import News


User = get_user_model()

@unittest.skip(reason='')
class TestNews(TestCase):
    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
        )

        cls.user = User.objects.create(username='testUser')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)

    def test_successful_creation(self):
        news_count = News.objects.count()

        self.assertEquals(news_count, 1)

    def test_title(self):
        self.assertEquals(self.news.title, self.TITLE)
