# Generated by Django 4.1 on 2022-09-22 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='date expired'),
        ),
    ]
