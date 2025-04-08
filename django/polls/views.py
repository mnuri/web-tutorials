from django.db.models import F, QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from polls.models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> QuerySet:
        return Question.published_objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question

    def get_queryset(self) -> QuerySet:
        return Question.published_objects.get_queryset()


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/question_results.html"

    def get_queryset(self) -> QuerySet:
        return Question.published_objects.get_queryset()


def vote(request, question_id) -> HttpResponseRedirect | HttpResponse:
    question: Question = get_object_or_404(Question.published_objects, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/question_detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
            status=422,
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
