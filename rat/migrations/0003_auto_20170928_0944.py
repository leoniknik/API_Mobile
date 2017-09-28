# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rat', '0002_testappnew'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual', models.BooleanField(db_index=True, default=True, verbose_name='actual')),
                ('date', models.TextField(null=True, verbose_name='crash_date')),
            ],
        ),
        migrations.CreateModel(
            name='CrashDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=24, unique=True, verbose_name='code')),
                ('full_description', models.TextField(default='', verbose_name='full_description')),
                ('short_description', models.TextField(default='', verbose_name='full_description')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, verbose_name='price')),
                ('message', models.TextField(default='', verbose_name='message')),
                ('date', models.TextField(default='', verbose_name='date')),
                ('is_avalible', models.BooleanField(db_index=True, default=False, verbose_name='is_avalible')),
                ('is_confirmed', models.BooleanField(db_index=True, default=False, verbose_name='is_confirmed')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TextField(default='', verbose_name='review_date')),
                ('text', models.TextField(default='', verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='name')),
                ('description', models.TextField(default='', verbose_name='description')),
                ('address', models.TextField(default='', verbose_name='address')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='phone')),
                ('email', models.TextField(default='', verbose_name='email')),
                ('longitude', models.FloatField(default=0.0, verbose_name='longitude')),
                ('latitude', models.FloatField(default=0.0, verbose_name='latitude')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('phone', models.CharField(default='', max_length=11, verbose_name='phone')),
                ('firstname', models.CharField(default='', max_length=255, verbose_name='firstname')),
                ('lastname', models.CharField(default='', max_length=255, verbose_name='lastname')),
            ],
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='vin',
            new_name='VIN',
        ),
        migrations.AddField(
            model_name='review',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rat.Service'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rat.User'),
        ),
        migrations.AddField(
            model_name='offer',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rat.Service'),
        ),
        migrations.AddField(
            model_name='offer',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rat.Vehicle'),
        ),
        migrations.AddField(
            model_name='crash',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rat.CrashDescription'),
        ),
        migrations.AddField(
            model_name='crash',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rat.Vehicle'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rat.User'),
        ),
    ]
