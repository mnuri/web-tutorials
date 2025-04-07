import pytest


# Root path


@pytest.mark.urls("fast_track.urls")
def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.content == b"I am root"


# Hello path


@pytest.mark.urls("fast_track.urls")
def test_processes_single_word_names(client):
    response = client.get("/hello/Bob")

    assert response.status_code == 200
    assert response.content == b"Hello Bob"


@pytest.mark.urls("fast_track.urls")
def test_handles_multi_word_names(client):
    response = client.get("/hello/Bob Bobson")

    assert response.status_code == 200
    assert response.content == b"Hello Bob Bobson"


@pytest.mark.urls("fast_track.urls")
def test_handles_very_long_name_inputs(client):
    response = client.get("/hello/" + "Bob" * 1000)

    assert response.status_code == 200
    assert response.content == b"Hello " + b"Bob" * 1000


@pytest.mark.urls("fast_track.urls")
def test_handles_empty_inputs(client):
    response = client.get("/hello/")

    assert response.status_code == 404
