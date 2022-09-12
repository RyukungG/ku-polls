import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """Question model for creating questions."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date expired', null=True, default=None, blank=True)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """Return boolean for it was published recently or not."""
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return boolean for the question was published or not."""
        now = timezone.localtime()
        return self.pub_date <= now

    def can_vote(self):
        """Return boolean for voting is allowed or not."""
        if self.end_date is None:
            return self.is_published()
        return self.pub_date <= timezone.localtime() <= self.end_date

    def __str__(self):
        """Return Question string."""
        return self.question_text


class Choice(models.Model):
    """Choice model for creating choices."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return Choice string."""
        return self.choice_text
