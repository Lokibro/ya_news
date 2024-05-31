from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news.models import Comment, News

User = get_user_model()


class TestRoute(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title='Заголовок',
            text='Текст'
        )
        cls.author = User.objects.create(
            username='Лев Толстой'
        )
        cls.reader = User.objects.create(
            username='Читатель простой'
        )
        cls.comment = Comment.objects.create(
            news = cls.news,
            author=cls.author,
            text='Текст комментария'
        )

    def test_pages_availability(self):
        urls = (
            ('news:home', None),
            ('news:detail', {'pk': self.news.id}),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None)
        )
        for name, kwargs in urls:
            with self.subTest(name=name):
                url = reverse(name, kwargs=kwargs)
                response = self.client.get(url)
                self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_availability_for_comment_edit_and_delete(self):
        user_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in user_statuses:
            self.client.force_login(user)
            for name in ('news:edit', 'news:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.comment.id,))
                    resource = self.client.get(url)
                    self.assertEquals(resource.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name in ('news:edit', 'news:delete'):
            with self.subTest(name=name):
                url = reverse(name, args=(self.comment.id,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)