# Generated by Django 5.0.6 on 2024-05-16 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buniwa', '0021_alter_portfoliopost_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='theFaqs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
        ),
    ]
