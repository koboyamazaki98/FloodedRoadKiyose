# Generated by Django 3.0.1 on 2020-01-14 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac01', '0004_auto_20200114_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='code',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
    ]
