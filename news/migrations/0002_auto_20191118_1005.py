# Generated by Django 2.2.7 on 2019-11-18 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='reference_app',
            field=models.CharField(choices=[('мфо', 'мфо'), ('кредитные_карты', 'кредитные_карты')], max_length=50, verbose_name='Приложение'),
        ),
        migrations.AlterField(
            model_name='news',
            name='reference_app',
            field=models.CharField(choices=[('мфо', 'мфо'), ('кредитные_карты', 'кредитные_карты')], max_length=50, verbose_name='Приложение'),
        ),
    ]
