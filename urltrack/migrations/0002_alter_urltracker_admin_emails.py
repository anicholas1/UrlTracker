# Generated by Django 3.2.4 on 2021-06-03 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urltrack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urltracker',
            name='admin_emails',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
