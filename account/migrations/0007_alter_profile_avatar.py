# Generated by Django 4.1 on 2022-09-09 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_profile_birth_date_profile_work_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(default='uploads/avatar/default.jpg', upload_to='uploads/avatar/', verbose_name='avatar'),
        ),
    ]
