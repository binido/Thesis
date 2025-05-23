# Generated by Django 5.2.1 on 2025-05-13 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_alter_article_status_alter_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/images/', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.URLField(blank=True, null=True, verbose_name='Источник'),
        ),
    ]
