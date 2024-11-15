# Generated by Django 4.2.13 on 2024-07-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buniwa', '0046_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'Users'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.AddField(
            model_name='profile',
            name='additional_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default_avatar.jpg', upload_to='profile_images/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='state_region',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_accounts',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
