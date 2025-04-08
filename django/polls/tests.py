import datetime

from django.contrib import admin
from django.urls import reverse
from django.utils import timezone

import pytest

from polls.admin import QuestionAdmin
from polls.models import Choice, Question


def create_question(question_text: str, days: int = 0) -> Question:
    time: datetime.datetime = timezone.now()

    if days:
        time += datetime.timedelta(days=days)

    return Question.objects.create(question_text=question_text, pub_date=time)


def create_question_with_choices(
    question_text: str, days: int = 0, choice_count: int = 2
) -> Question:
    question: Question = create_question(question_text, days)

    for i in range(choice_count):
        question.choice_set.create(choice_text=f"Choice {i}", votes=0)

    return question


# Question admin model


question_admin = QuestionAdmin(Question, admin.site)


def test_was_published_recently_with_future_question():
    time: datetime.datetime = timezone.now() + datetime.timedelta(days=30)
    future_question: Question = Question(pub_date=time)

    assert question_admin.was_published_recently(future_question) is False


def test_was_published_recently_with_old_question():
    time: datetime.datetime = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question: Question = Question(pub_date=time)

    assert question_admin.was_published_recently(old_question) is False


def test_was_published_recently_with_recent_question():
    time: datetime.datetime = timezone.now() - datetime.timedelta(
        hours=23, minutes=59, seconds=59
    )
    recent_question: Question = Question(pub_date=time)

    assert question_admin.was_published_recently(recent_question) is True


# Question model


@pytest.mark.django_db
def test_published_objects_manager():
    question: Question = create_question("Does the sky look blue?", 0)
    assert Question.published_objects.get(pk=question.pk)

    question = create_question("Does the sky look green?", 1)
    with pytest.raises(Question.DoesNotExist):
        Question.published_objects.get(pk=question.pk)


# Question view index

polls_path: str = reverse("polls:index")


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_index_with_no_questions(client):
    response = client.get(polls_path)

    assert response.status_code == 200
    assert b"No polls are available." in response.content
    assert not response.context["latest_question_list"]


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_index_with_a_past_question(client):
    question: Question = create_question("Does the sky look blue?", -1)
    response = client.get(polls_path)

    assert response.status_code == 200
    assert question.question_text.encode() in response.content
    assert list(response.context["latest_question_list"]) == [question]


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_index_with_a_future_question(client):
    create_question("Does the sky look blue?", 1)
    response = client.get(polls_path)

    assert response.status_code == 200
    assert b"No polls are available." in response.content
    assert not response.context["latest_question_list"]


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_index_with_future_and_past_questions(client):
    past_question: Question = create_question("Does the sky look blue?", -1)
    create_question("Does the sky look green?", 1)
    response = client.get(polls_path)

    assert response.status_code == 200
    assert past_question.question_text.encode() in response.content
    assert list(response.context["latest_question_list"]) == [past_question]


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_index_with_two_past_questions(client):
    past_question1: Question = create_question("Does the sky look blue?", -1)
    past_question2: Question = create_question("Does the sky look green?", -2)
    response = client.get(polls_path)

    assert response.status_code == 200
    assert past_question1.question_text.encode() in response.content
    assert past_question2.question_text.encode() in response.content

    assert list(response.context["latest_question_list"]) == [
        past_question1,
        past_question2,
    ]


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_index_with_current_time_question(client):
    question: Question = create_question("Does the sky look blue?", 0)
    response = client.get(polls_path)

    assert response.status_code == 200
    assert question.question_text.encode() in response.content

    assert list(response.context["latest_question_list"]) == [question]


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_index_with_limit(client):
    words: list[str] = ["blue", "green", "red", "yellow", "black", "white"]

    questions: list[Question] = [
        create_question(f"Does the sky look {word}", -i) for i, word in enumerate(words)
    ]

    response = client.get(polls_path)

    assert response.status_code == 200
    assert list(response.context["latest_question_list"]) == questions[:5]


# Question view detail


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_detail_with_future_question(client):
    future_question: Question = create_question("Does the sky look blue?", 5)
    url: str = reverse("polls:detail", args=(future_question.id,))
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_detail_with_past_question(client):
    past_question: Question = create_question("Does the sky look blue?", -5)
    url: str = reverse("polls:detail", args=(past_question.id,))
    response = client.get(url)

    assert response.status_code == 200
    assert past_question.question_text.encode() in response.content


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_detail_with_choices(client):
    question: Question = create_question_with_choices("Does the sky look blue?", 0, 2)
    url: str = reverse("polls:detail", args=(question.id,))
    response = client.get(url)

    assert response.status_code == 200
    assert question.question_text.encode() in response.content

    for choice in question.choice_set.all():
        assert choice.choice_text.encode() in response.content


# Question view results


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_results_with_future_question(client):
    future_question: Question = create_question("Does the sky look blue?", 5)
    url: str = reverse("polls:results", args=(future_question.id,))
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_results_with_past_question(client):
    past_question: Question = create_question("Does the sky look blue?", -5)
    url: str = reverse("polls:results", args=(past_question.id,))
    response = client.get(url)

    assert response.status_code == 200
    assert past_question.question_text.encode() in response.content


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_results_with_choices(client):
    question: Question = create_question("Does the sky look blue?", 0)

    Choice.objects.create(question=question, choice_text="Yes", votes=10)
    Choice.objects.create(question=question, choice_text="No", votes=5)

    url: str = reverse("polls:results", args=(question.id,))
    response = client.get(url)

    assert response.status_code == 200
    assert question.question_text.encode() in response.content

    assert b"Yes -- 10 votes" in response.content
    assert b"No -- 5 votes" in response.content


# Question view vote


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_vote_with_future_question(client):
    future_question: Question = create_question("Does the sky look blue?", 5)
    url: str = reverse("polls:vote", args=(future_question.id,))
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_vote_with_past_question(client):
    question: Question = create_question("Does the sky look blue?", -5)
    choice_first: Choice = Choice.objects.create(question=question, choice_text="Yes")
    choice_second: Choice = Choice.objects.create(question=question, choice_text="No")

    url: str = reverse("polls:vote", args=(question.id,))
    response = client.post(url, {"choice": choice_first.id})

    assert response.status_code == 302
    assert response.url == reverse("polls:results", args=(question.id,))

    choice_first.refresh_from_db()
    choice_second.refresh_from_db()

    assert choice_first.votes == 1
    assert choice_second.votes == 0


@pytest.mark.django_db
@pytest.mark.urls("fast_track.urls")
def test_polls_vote_with_invalid_choice(client):
    question: Question = create_question("Does the sky look blue?", -5)

    Choice.objects.create(question=question, choice_text="Yes")

    url: str = reverse("polls:vote", args=(question.id,))
    response = client.post(url, {"choice": 0})

    assert response.status_code == 422
    assert b"You didn&#x27;t select a choice." in response.content
