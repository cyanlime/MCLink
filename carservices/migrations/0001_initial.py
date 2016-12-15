# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-15 18:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(max_length=200)),
                ('token', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WXUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('head_portrait', models.URLField()),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carservices.Account')),
            ],
        ),
    ]
