# Generated by Django 4.1.1 on 2022-09-12 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(default='default.jpg', upload_to='', verbose_name='avatar'),
        ),
    ]
