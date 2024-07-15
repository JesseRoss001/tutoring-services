# Generated by Django 5.0.6 on 2024-07-15 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_availablehour_booked_by_availablehour_cost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availablehour',
            name='booked_by',
        ),
        migrations.RemoveField(
            model_name='availablehour',
            name='cost',
        ),
        migrations.AddField(
            model_name='availablehour',
            name='is_recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='availablehour',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]
