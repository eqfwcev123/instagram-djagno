# Generated by Django 2.2.9 on 2020-01-14 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200114_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='posts.Tag', verbose_name='해시태그 목록'),
        ),
    ]
