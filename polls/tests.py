import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Question, Vote


def create_question(question_text, days, end=None):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    endtime = end
    if end != None:
        endtime = timezone.now() + datetime.timedelta(days=end)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=endtime)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() return False
        for questions whose pub_date is not arrived.
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_past_question(self):
        """
        is_published() return True
        for questions whose pub_date are already passed.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        past_question = Question(pub_date=time)
        self.assertTrue(past_question.is_published())

    def test_can_vote_with_current_question(self):
        """
        can_vote() return True
        for questions whose current time are within the pub_date and end_date.
        """
        past = timezone.now() - timezone.timedelta(hours=1)
        future = timezone.now() + timezone.timedelta(hours=1)
        question = Question(pub_date=past, end_date=future)
        self.assertTrue(question.can_vote())

    def test_can_vote_with__future_question(self):
        """
        can_vote() return False for questions whose pub_date is not arrived.
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.can_vote())

    def test_can_vote_with_expired_question(self):
        """
        can_voted() return False
        for questions whose end_date are already passed.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        end_time = timezone.now() - datetime.timedelta(hours=1)
        past_question = Question(pub_date=time, end_date=end_time)
        self.assertFalse(past_question.can_vote())

    def test_can_vote_with_none_end_date_question(self):
        """
        can_vote() return True
        for questions whose not have end_date.
        """
        past = timezone.now() - timezone.timedelta(hours=1)
        question = Question(pub_date=past)
        self.assertTrue(question.can_vote())


class VoteModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user("test", "test@mail.com", "tttttttt")
        user.save()

    def test_unauthenticated_vote(self):
        """test if unauthenticated user vote
        it should redirect to login page."""
        question = Question.objects.create(question_text="Test",
                                           pub_date=timezone.now())
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_authenticate_vote(self):
        """test authenticate user can vote."""
        self.client.login(username="test", password="tttttttt")
        question = Question.objects.create(question_text="Test",
                                           pub_date=timezone.now())
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):

    def setUp(self):
        user = User.objects.create_user("test", "test@mail.com", "tttttttt")
        user.save()
        self.client.login(username="test", password="tttttttt")

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_end_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302.
        """
        end_question = create_question(question_text='End question.',
                                          days=-5, end=-3)
        url = reverse('polls:detail', args=(end_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class QuestionResultViewTests(TestCase):
    def test_current_question(self):
        """
        Questions with a pub_date in the future can see result.
        """
        past_question = create_question(question_text="Past question.",
                                        days=-30)
        response = self.client.get(reverse('polls:results',
                                           args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)

    def test_future_question(self):
        """
        Questions with a pub_date in the future can't see result.
        """
        future_question = create_question(question_text="Future question.",
                                          days=30)
        response = self.client.get(reverse('polls:results',
                                           args=(future_question.id,)))
        self.assertEqual(response.status_code, 302)

class QuestionVoteViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user("test", "test@mail.com", "tttttttt")
        self.user.save()

    def test_one_person_one_vote(self):
        """One user can vote once per question."""
        self.client.login(username="test", password="tttttttt")
        question = create_question(question_text="test", days=-10)
        choice_test1 = question.choice_set.create(choice_text="one")
        choice_test2 = question.choice_set.create(choice_text="two")
        self.client.post(reverse('polls:vote', args=(question.id,)),
                         {'choice': choice_test1.id})
        selected = Vote.objects.get(user=self.user,
                                    choice__in=question.choice_set.all())
        self.assertEqual(selected.choice, choice_test1)
        self.assertEqual(Vote.objects.all().count(), 1)

        self.client.post(reverse('polls:vote', args=(question.id,)),
                         {'choice': choice_test2.id})
        selected = Vote.objects.get(user=self.user,
                                    choice__in=question.choice_set.all())
        self.assertEqual(selected.choice, choice_test2)
        self.assertEqual(Vote.objects.all().count(), 1)

