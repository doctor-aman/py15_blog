# Generated by Django 4.0 on 2022-01-07 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_activation_code'),
        ('main', '0005_alter_favorite_unique_together'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Favorite',
            new_name='Favorites',
        ),
    ]