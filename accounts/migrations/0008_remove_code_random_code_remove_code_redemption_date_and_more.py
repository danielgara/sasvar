# Generated by Django 5.0 on 2024-02-13 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_userhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='random_code',
        ),
        migrations.RemoveField(
            model_name='code',
            name='redemption_date',
        ),
        migrations.RemoveField(
            model_name='code',
            name='used_by_user',
        ),
        migrations.AddField(
            model_name='code',
            name='consecutive',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='code',
            name='id_container',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='code',
            name='id_model',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='code',
            name='id_physical_location',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='code',
            name='material',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='code',
            name='success',
            field=models.IntegerField(choices=[(0, 'Failure'), (1, 'Success')], default=0),
            preserve_default=False,
        ),
    ]
