# Generated by Django 5.0.6 on 2024-07-11 22:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_availablehour_is_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('max_participants', models.PositiveIntegerField()),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
            ],
        ),
        migrations.RenameField(
            model_name='livestream',
            old_name='url',
            new_name='link',
        ),
        migrations.RemoveField(
            model_name='livestream',
            name='course',
        ),
        migrations.RemoveField(
            model_name='session',
            name='course',
        ),
        migrations.AddField(
            model_name='livestream',
            name='description',
            field=models.TextField(default='No description provided'),
        ),
        migrations.AlterField(
            model_name='availablehour',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='livestream',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='CourseSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('max_participants', models.PositiveIntegerField()),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
            ],
        ),
        migrations.DeleteModel(
            name='RecordedCourse',
        ),
    ]
