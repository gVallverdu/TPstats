# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 23:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='TP 03/12/16', max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Glassware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('glassware', models.CharField(choices=[('BE', 'Becher'), ('FI', 'Fiole jaugée'), ('BU', 'Burette'), ('EP', 'Éprouvette'), ('PI', 'Pipette')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collectDatas.Experiment')),
                ('glassware', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collectDatas.Glassware')),
            ],
        ),
    ]