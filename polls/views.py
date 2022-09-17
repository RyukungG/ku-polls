from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    """Index page of application."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail page of application."""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, pk):
        """Return different pages in accordance to can_vote and is_published."""
        question = get_object_or_404(Question, pk=pk)
        if not question.is_published():
            messages.error(request, 'This poll not publish yet.')
            return HttpResponseRedirect(reverse('polls:index'))
        elif not question.can_vote():
            messages.error(request, 'This poll is ended.')
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'polls/detail.html', {'question': question, })


class ResultsView(generic.DetailView):
    """Result page of the application."""
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, pk):
        """Return result page if can_vote method returns True. If not then redirect to results page."""
        question = get_object_or_404(Question, pk=pk)
        if not question.is_published():
            messages.error(request, 'This poll not publish yet.')
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'polls/results.html', {'question': question})


@login_required
def vote(request, question_id):
    """Add vote to choice of the current question."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
