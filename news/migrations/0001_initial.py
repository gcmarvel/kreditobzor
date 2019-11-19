# Generated by Django 2.2.7 on 2019-11-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000, verbose_name='Заголовок')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Текст')),
                ('reference_app', models.CharField(choices=[('мфо', 'мфо'), ('кредитные_карты', 'кредитные_карты')], max_length=50)),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000, verbose_name='Заголовок')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Текст')),
                ('reference_app', models.CharField(choices=[('мфо', 'мфо'), ('кредитные_карты', 'кредитные_карты')], max_length=50)),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
