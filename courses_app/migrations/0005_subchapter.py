# Generated by Django 5.1.4 on 2024-12-15 15:10

import django.db.models.deletion
import embed_video.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0004_lesson'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subchapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('video', embed_video.fields.EmbedVideoField(blank=True, null=True)),
                ('Sub', models.ManyToManyField(related_name='chapters', to='courses_app.lesson')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]