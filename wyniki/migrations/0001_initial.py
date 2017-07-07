# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kandydat',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('numerKandydata', models.CharField(max_length=100)),
                ('imieINazwisko', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Wynik',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('wojewodztwo', models.CharField(max_length=100)),
                ('okreg', models.CharField(max_length=100)),
                ('powiat', models.CharField(max_length=100)),
                ('gmina', models.CharField(max_length=100)),
                ('w1', models.FloatField(default=0)),
                ('w2', models.FloatField(default=0)),
                ('w3', models.FloatField(default=0)),
                ('w4', models.FloatField(default=0)),
                ('w5', models.FloatField(default=0)),
                ('w6', models.FloatField(default=0)),
                ('w7', models.FloatField(default=0)),
                ('w8', models.FloatField(default=0)),
                ('w9', models.FloatField(default=0)),
                ('w10', models.FloatField(default=0)),
                ('w11', models.FloatField(default=0)),
                ('w12', models.FloatField(default=0)),
                ('uprawnionych', models.IntegerField(default=0)),
                ('wydanych_kart', models.IntegerField(default=0)),
                ('wyjetych_kart', models.IntegerField(default=0)),
                ('niewaznych_glosow', models.IntegerField(default=0)),
                ('waznych_glosow', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WynikZPost',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('w1', models.FloatField(default=0)),
                ('w2', models.FloatField(default=0)),
                ('w3', models.FloatField(default=0)),
                ('w4', models.FloatField(default=0)),
                ('w5', models.FloatField(default=0)),
                ('w6', models.FloatField(default=0)),
                ('w7', models.FloatField(default=0)),
                ('w8', models.FloatField(default=0)),
                ('w9', models.FloatField(default=0)),
                ('w10', models.FloatField(default=0)),
                ('w11', models.FloatField(default=0)),
                ('w12', models.FloatField(default=0)),
            ],
        ),
    ]
