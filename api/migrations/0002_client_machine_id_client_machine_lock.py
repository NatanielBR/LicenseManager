# Generated by Django 5.1.6 on 2025-03-09 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='machine_id',
            field=models.CharField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='client',
            name='machine_lock',
            field=models.BooleanField(default=False),
        ),
    ]
