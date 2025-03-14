# Generated by Django 5.1.5 on 2025-03-04 22:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_input', models.TextField()),
                ('ai_response', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
