# Generated by Django 4.2.3 on 2023-07-27 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=150, verbose_name='место')),
                ('time', models.TimeField(verbose_name='время')),
                ('action', models.CharField(max_length=150, unique=True, verbose_name='действие')),
                ('duration', models.PositiveIntegerField(default=120, verbose_name='длительность выполнений в секундах')),
                ('is_published', models.BooleanField(default=True, verbose_name='признак публичности привычки')),
            ],
        ),
        migrations.CreateModel(
            name='GoodHabit',
            fields=[
                ('habit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='habit_tracker.habit')),
                ('reward', models.TextField(blank=True, null=True, verbose_name='вознаграждение')),
                ('frequency', models.CharField(choices=[('EVERY DAY', 'раз в день'), ('EVERY OTHER DAY', 'через день'), ('EVERY WEEK', 'раз в неделю')], default='EVERY DAY', max_length=100, verbose_name='Периодичность')),
            ],
            options={
                'verbose_name': 'полезная привычка',
                'verbose_name_plural': 'полезные привычки',
            },
            bases=('habit_tracker.habit',),
        ),
        migrations.CreateModel(
            name='PleasantHabit',
            fields=[
                ('habit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='habit_tracker.habit')),
                ('is_pleasant_habit', models.BooleanField(default=True, verbose_name='признак приятной привычки')),
            ],
            options={
                'verbose_name': 'приятная привычка',
                'verbose_name_plural': 'приятные привычки',
            },
            bases=('habit_tracker.habit',),
        ),
    ]
