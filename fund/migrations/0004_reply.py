# Generated by Django 5.1.6 on 2025-02-24 23:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0003_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='fund.comment')),
                ('written_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='fund.user')),
            ],
            options={
                'verbose_name_plural': 'replies',
                'ordering': ('created_at',),
            },
        ),
    ]
