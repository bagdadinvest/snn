# Generated by Django 5.1.2 on 2024-11-01 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_pricingsnippet_partnersnippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='CounterSnippet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procedure', models.CharField(help_text='Name of the procedure (e.g., Makeup Over Done).', max_length=255)),
                ('number', models.PositiveIntegerField(help_text='Number to display for the counter.')),
            ],
        ),
    ]
