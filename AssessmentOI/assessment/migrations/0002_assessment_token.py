# Generated by Django 3.2.1 on 2021-05-10 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='token',
            field=models.EmailField(blank=True, max_length=256, null=True),
        ),
    ]
