# Generated by Django 4.2.7 on 2025-05-29 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('genre', models.CharField(choices=[('ACTION', 'Action'), ('COMEDY', 'Comedy'), ('DRAMA', 'Drama'), ('HORROR', 'Horror'), ('ROMANCE', 'Romance'), ('THRILLER', 'Thriller'), ('SCI_FI', 'Science Fiction'), ('FANTASY', 'Fantasy'), ('ANIMATION', 'Animation'), ('DOCUMENTARY', 'Documentary')], max_length=20)),
                ('rating', models.CharField(choices=[('G', 'General Audiences'), ('PG', 'Parental Guidance'), ('PG_13', 'PG-13'), ('R', 'Restricted'), ('NC_17', 'Adults Only')], max_length=10)),
                ('duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('release_date', models.DateField()),
                ('poster', models.ImageField(blank=True, null=True, upload_to='movie_posters/')),
                ('trailer_url', models.URLField(blank=True, null=True)),
                ('director', models.CharField(max_length=100)),
                ('cast', models.TextField(help_text='Comma-separated list of main cast')),
                ('language', models.CharField(default='English', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-release_date'],
            },
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('total_seats', models.PositiveIntegerField()),
                ('rows', models.PositiveIntegerField(default=10)),
                ('seats_per_row', models.PositiveIntegerField(default=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_date', models.DateField()),
                ('show_time', models.TimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('available_seats', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='showtimes', to='movies.movie')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='showtimes', to='movies.theater')),
            ],
            options={
                'ordering': ['show_date', 'show_time'],
                'unique_together': {('theater', 'show_date', 'show_time')},
            },
        ),
    ]
