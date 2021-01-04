# Generated by Django 3.1.3 on 2021-01-04 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_auto_20201219_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('post', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tmp',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('rainfall', models.FloatField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tmp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tmp2',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(blank=True, db_column='Year', null=True)),
                ('month', models.IntegerField(blank=True, db_column='Month', null=True)),
                ('rainfall', models.FloatField(blank=True, db_column='Rainfall', null=True)),
                ('location', models.TextField(blank=True, db_column='Location', null=True)),
            ],
            options={
                'db_table': 'tmp2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tmp3',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(blank=True, db_column='Year', null=True)),
                ('month', models.IntegerField(blank=True, db_column='Month', null=True)),
                ('rainfall', models.FloatField(blank=True, db_column='Rainfall', null=True)),
                ('location', models.TextField(blank=True, db_column='Location', null=True)),
            ],
            options={
                'db_table': 'tmp3',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tmp4',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(blank=True, db_column='Year', null=True)),
                ('month', models.IntegerField(blank=True, db_column='Month', null=True)),
                ('rainfall', models.FloatField(blank=True, db_column='Rainfall', null=True)),
                ('location', models.TextField(blank=True, db_column='Location', null=True)),
            ],
            options={
                'db_table': 'tmp4',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tmp5',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(blank=True, db_column='Year', null=True)),
                ('month', models.IntegerField(blank=True, db_column='Month', null=True)),
                ('rainfall', models.FloatField(blank=True, db_column='Rainfall', null=True)),
                ('location', models.TextField(blank=True, db_column='Location', null=True)),
            ],
            options={
                'db_table': 'tmp5',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='post',
            table='post',
        ),
    ]
