# Generated by Django 4.2 on 2023-05-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_store_app', '0003_alter_user_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=20),
        ),
    ]
