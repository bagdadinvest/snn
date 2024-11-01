# Generated by Django 5.1.2 on 2024-11-01 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_homepage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='appointment_info_text',
        ),
        migrations.AddField(
            model_name='homepage',
            name='appointment_address',
            field=models.TextField(blank=True, help_text='Address displayed in the appointment section.'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='appointment_opening_hours',
            field=models.CharField(blank=True, help_text='Opening hours displayed in the appointment section.', max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='appointment_phone_primary',
            field=models.CharField(blank=True, help_text='Primary phone number displayed in the appointment section.', max_length=20),
        ),
        migrations.AddField(
            model_name='homepage',
            name='appointment_phone_secondary',
            field=models.CharField(blank=True, help_text='Secondary phone number displayed in the appointment section.', max_length=20),
        ),
    ]
