from django.urls import reverse

import pytest


# Home path

home_path = reverse("home:home")


@pytest.mark.urls("fast_track.urls")
def test_home_page(client):
    response = client.get(home_path)

    assert response.status_code == 200
    assert b"Home" in response.content
    assert b"Polls" in response.content


# Hello path

hello_path = reverse("home:hello")


@pytest.mark.urls("fast_track.urls")
def test_get_hello_page(client):
    response = client.get(hello_path)

    assert response.status_code == 200
    assert b"Enter a name" in response.content


@pytest.mark.urls("fast_track.urls")
def test_post_hello_page(client):
    response = client.post(hello_path, {"hello_name": "Bob"})

    assert response.status_code == 302
    assert response.url == "/hello/Bob/"


@pytest.mark.urls("fast_track.urls")
def test_invalid_post_hello_page(client):
    response = client.post(hello_path, {"hello_name": ""})

    assert response.status_code == 422
    assert b"You didn&#x27;t enter a name." in response.content


# Say Hello path


def say_hello_path(name):
    return reverse("home:say_hello", args=(name,))


@pytest.mark.urls("fast_track.urls")
def test_say_hello_page(client):
    response = client.get(say_hello_path("Bob"))

    assert response.status_code == 200
    assert b"Hello Bob" in response.content


@pytest.mark.urls("fast_track.urls")
def test_say_hello_page_with_multiple_words(client):
    response = client.get(say_hello_path("Bob Bobson"))

    assert response.status_code == 200
    assert b"Hello Bob Bobson" in response.content


@pytest.mark.urls("fast_track.urls")
def test_say_hello_page_with_very_long_name(client):
    response = client.get(say_hello_path("Bob" * 1000))

    assert response.status_code == 200
    assert b"Hello " + b"Bob" * 1000 in response.content
