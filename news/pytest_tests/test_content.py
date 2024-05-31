import pytest

from django.test import Client
from django.urls import reverse

import yanews.settings
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(list_news, author):
    url = reverse('news:home')
    client = Client()
    response = client.get(url)
    news_count = response.context['object_list'].count()
    assert news_count == yanews.settings.NEWS_COUNT_ON_HOME_PAGE

# test_news_order
# test_comments_order
# test_anonymous_client_has_no_form
# test_authorized_client_has_form

