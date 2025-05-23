# Generated by Django 4.2.20 on 2025-04-18 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.CharField(max_length=100, primary_key='True', serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.CharField(max_length=50, primary_key='True', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('shortname', models.CharField(default='X', max_length=50)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.dept')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('term', models.CharField(blank=True, choices=[('First Term', 'First Term'), ('Second Term', 'Second Term'), ('Third Term', 'Third Term'), ('Others', 'Others')], default='First Term', max_length=15, null=True)),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('desc', models.TextField(blank=True, max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('name', 'term')},
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.CharField(max_length=100, primary_key='True', serialize=False)),
                ('section', models.CharField(max_length=100)),
                ('sem', models.IntegerField()),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.dept')),
            ],
            options={
                'verbose_name_plural': 'classes',
            },
        ),
    ]
