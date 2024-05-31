from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from django.test import Client
from django.urls import reverse

from news.models import News, Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news, form_data, client, id_for_args):
    url = reverse('news:detail', args=id_for_args)
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(news, not_author_client, form_data, id_for_args):
    url = reverse('news:detail', args=id_for_args)
    response = not_author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    comment_from_db = Comment.objects.get()
    assert comment_from_db.news == form_data['news']
    assert comment_from_db.text == form_data['text']


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, news, id_for_args):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, ещё текст'}
    url = reverse('news:detail', args=id_for_args)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, comment, news, id_for_args):
    url_delete = reverse('news:delete', args=(comment.news.pk,))
    url_detail = reverse('news:detail', args=id_for_args)
    response = author_client.delete(url_delete)
    assertRedirects(response, f'{url_detail}#comments')
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
        not_author_client, news, comment, id_for_args):
    url_delete = reverse('news:delete', args=(comment.news.pk,))
    response = not_author_client.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_author_can_edit_comment(
        author_client, news, comment, id_for_args, form_data):
    url_edit = reverse('news:edit', args=(comment.news.pk,))
    url_detail = reverse('news:detail', args=id_for_args)
    response = author_client.post(url_edit, data=form_data)
    assertRedirects(response, f'{url_detail}#comments')
    comment_from_db = Comment.objects.get()
    assert form_data['text'] == comment_from_db.text


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
        not_author_client, news, comment, id_for_args, form_data):
    url_edit = reverse('news:edit', args=(comment.news.pk,))
    response = not_author_client.post(url_edit, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get()
    assert comment.text == comment_from_db.text
