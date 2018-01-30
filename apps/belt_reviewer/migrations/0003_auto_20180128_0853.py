# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-28 08:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_reviewer', '0002_book_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=255)),
                ('last', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='belt_reviewer.Book'),
        ),
    ]
