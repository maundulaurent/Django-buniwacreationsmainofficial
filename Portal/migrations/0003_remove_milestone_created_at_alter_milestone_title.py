# Generated by Django 4.2.13 on 2024-07-10 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0002_milestone_projectrequest_theadmin_theclient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='milestone',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
