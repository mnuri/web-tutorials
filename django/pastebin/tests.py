import json

from django.urls import reverse

import pytest

from pastebin.models import Snippet


@pytest.fixture(name="authorized_user")
def authorized_user_fixture(django_user_model):
    return django_user_model.objects.create_user(username="test", password="test")


@pytest.fixture(name="sample_user")
def sample_user_fixture(django_user_model):
    return django_user_model.objects.create_user(username="sample", password="test")


@pytest.fixture(name="authorized_client")
def authorized_client_fixture(client, authorized_user):
    client.force_login(authorized_user)
    return client


# GET /

api_root_path = reverse("api-root")


@pytest.mark.django_db
def test_index(client):
    response = client.get(api_root_path)
    assert response.status_code == 200


# GET /users/

user_index_path = reverse("user-list")


@pytest.mark.django_db
def test_users_index(client):
    response = client.get(user_index_path)
    assert response.status_code == 403


@pytest.mark.django_db
def test_users_index_authorized(authorized_client):
    response = authorized_client.get(user_index_path)
    assert response.status_code == 200


# POST /users/


@pytest.mark.django_db
def test_create_user(client):
    response = client.post(user_index_path, {"username": "test2", "password": "test2"})

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_user_authorized(authorized_client):
    response = authorized_client.post(
        user_index_path, {"username": "test2", "password": "test2"}
    )

    assert response.status_code == 405


# GET /users/{id}


@pytest.mark.django_db
def test_users_detail(client, sample_user):
    url: str = reverse("user-detail", args=(sample_user.id,))
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_users_detail_authorized(authorized_client, authorized_user):
    url: str = reverse("user-detail", args=(authorized_user.id,))
    response = authorized_client.get(url)

    assert response.status_code == 200


# DELETE /users/{id}


@pytest.mark.django_db
def test_delete_user(client, sample_user):
    url: str = reverse("user-detail", args=(sample_user.id,))
    response = client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_user_authorized(authorized_client, authorized_user):
    url: str = reverse("user-detail", args=(authorized_user.id,))
    response = authorized_client.delete(url)

    assert response.status_code == 405


# GET /groups/

group_index_path = reverse("group-list")


@pytest.mark.django_db
def test_groups_index(client):
    response = client.get(group_index_path)
    assert response.status_code == 403


@pytest.mark.django_db
def test_groups_index_authorized(authorized_client):
    response = authorized_client.get(group_index_path)
    assert response.status_code == 200


# GET /snippets/

snippet_index_path = reverse("snippet-list")


@pytest.mark.django_db
def test_snippets_index(client):
    response = client.get(snippet_index_path)
    assert response.status_code == 200


# POST /snippets/


@pytest.mark.django_db
def test_snippets_create(client):
    response = client.post(snippet_index_path, {"title": "test", "code": "test"})
    assert response.status_code == 403


@pytest.mark.django_db
def test_snippets_create_authorized(authorized_client):
    response = authorized_client.post(
        snippet_index_path, {"title": "test", "code": "test"}
    )
    assert response.status_code == 201


# GET /snippets/{id}


@pytest.mark.django_db
def test_snippets_detail(client, sample_user):
    snippet = Snippet.objects.create(title="test", code="test", owner=sample_user)
    url = reverse("snippet-detail", args=(snippet.id,))
    response = client.get(url)

    assert response.status_code == 200


# PUT /snippets/{id}/

sample_data = {"title": "test2", "code": "test2"}


@pytest.mark.django_db
def test_snippets_update(client, sample_user):
    snippet = Snippet.objects.create(title="test", code="test", owner=sample_user)
    url = reverse("snippet-detail", args=(snippet.id,))
    response = client.put(url, {"title": "test2", "code": "test2"})

    assert response.status_code == 403


@pytest.mark.django_db
def test_snippets_update_authorized_with_alien_snippet(authorized_client, sample_user):
    snippet = Snippet.objects.create(title="test", code="test", owner=sample_user)
    url = reverse("snippet-detail", args=(snippet.id,))
    response = authorized_client.put(
        url, data=json.dumps(sample_data), content_type="application/json"
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_snippets_update_authorized_with_his_snippet(
    authorized_client, authorized_user
):
    snippet = Snippet.objects.create(title="test", code="test", owner=authorized_user)
    url = reverse("snippet-detail", args=(snippet.id,))
    response = authorized_client.put(
        url, data=json.dumps(sample_data), content_type="application/json"
    )

    assert response.status_code == 200


# DELETE /snippets/{id}/


@pytest.mark.django_db
def test_snippets_delete(client, sample_user):
    snippet = Snippet.objects.create(title="test", code="test", owner=sample_user)
    url = reverse("snippet-detail", args=(snippet.id,))
    response = client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_snippets_delete_authorized_with_alien_snippet(authorized_client, sample_user):
    snippet = Snippet.objects.create(title="test", code="test", owner=sample_user)
    url = reverse("snippet-detail", args=(snippet.id,))
    response = authorized_client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_snippets_delete_authorized_with_his_snippet(
    authorized_client, authorized_user
):
    snippet = Snippet.objects.create(title="test", code="test", owner=authorized_user)
    url = reverse("snippet-detail", args=(snippet.id,))
    response = authorized_client.delete(url)

    assert response.status_code == 204


# GET /snippets/{id}/highlight/


@pytest.mark.django_db
def test_snippets_highlight(client, sample_user):
    snippet = Snippet.objects.create(title="test", code="test", owner=sample_user)
    url = reverse("snippet-highlight", args=(snippet.id,))
    response = client.get(url)

    assert response.status_code == 200
