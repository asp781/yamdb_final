# Generated by Django 2.2.16 on 2022-09-13 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220913_1548'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('author', 'title')},
        ),
    ]
