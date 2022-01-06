# Generated by Django 4.0.1 on 2022-01-05 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('year', models.IntegerField(blank=True)),
                ('num', models.IntegerField(default=0)),
                ('i_watchlist', models.BooleanField(default=False)),
                ('i_watched', models.BooleanField(default=False)),
                ('o_watchlist', models.BooleanField(default=False)),
                ('o_watched', models.BooleanField(default=False)),
            ],
        ),
    ]