# Generated by Django 5.0.6 on 2024-07-11 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_session_event_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='capacity',
        ),
        migrations.AddField(
            model_name='session',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='session',
            name='event_type',
            field=models.CharField(choices=[('1-to-1', '1-to-1'), ('group', 'Group'), ('live_stream', 'Live Stream'), ('testing', 'Testing')], max_length=20),
        ),
        migrations.AlterField(
            model_name='session',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.student'),
        ),
    ]
