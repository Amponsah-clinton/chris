# Generated by Django 4.2.4 on 2023-08-14 07:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_comment_delete_rating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Comments',
        ),
    ]
