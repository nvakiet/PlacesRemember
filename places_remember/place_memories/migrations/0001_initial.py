# Generated by Django 4.1 on 2023-02-05 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('social_django', '0010_uid_db_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMemories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placename', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_django.usersocialauth')),
            ],
        ),
    ]
