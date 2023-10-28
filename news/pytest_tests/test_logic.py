from http import HTTPStatus
import pytest
from django.urls import reverse
from news.models import Comment, News
from news.forms import WARNING
from pytest_django.asserts import assertRedirects, assertFormError


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client,
    id_news_for_args,
    form_data
):
    url = reverse('news:detail', args=id_news_for_args)
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
    author_client,
    author,
    id_news_for_args,
    form_data,

):
    url = reverse('news:detail', args=id_news_for_args)
    author_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.author == author


def test_user_cant_use_bad_words(
    author_client,
    author,
    id_news_for_args,
    bad_form_data,
):
    url = reverse('news:detail', args=id_news_for_args)
    response = author_client.post(url, data=bad_form_data)
    comments_count = Comment.objects.count()
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert comments_count == 0
    

def test_author_can_delete_comment(
    author_client,
    id_comment_for_args,
    id_news_for_args

):
    delete_url = reverse('news:delete', args=id_comment_for_args)
    url_to_comments = reverse(
        'news:detail',
        args=id_news_for_args
    ) + '#comments'
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    id_comment_for_args,
    reader_client,
):
    delete_url = reverse('news:delete', args=id_comment_for_args)
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
    author_client,
    id_comment_for_args,
    id_news_for_args,
    form_data,
    comment
):
    edit_url = reverse('news:edit', args=id_comment_for_args)
    url_to_comments = reverse(
        'news:detail',
        args=id_news_for_args
    ) + '#comments'
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']

@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    id_comment_for_args,
    reader_client,
    comment,
    form_data
):
    edit_url = reverse('news:edit', args=id_comment_for_args)
    prev_text_comment = comment.text
    response = reader_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == prev_text_comment
