# Generated by Django 2.2.7 on 2019-11-15 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mfo', '0011_auto_20191115_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='rating'),
        ),
    ]
