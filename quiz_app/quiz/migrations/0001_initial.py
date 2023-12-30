# Generated by Django 4.2.1 on 2023-12-26 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quiz_file', models.FileField(upload_to='quiz/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('upadated_at', models.DateTimeField(auto_now=True)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quiz.category')),
            ],
        ),
    ]