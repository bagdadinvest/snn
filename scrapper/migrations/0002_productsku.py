# Generated by Django 5.1.2 on 2024-11-05 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sku', models.CharField(max_length=20, unique=True)),
                ('constructed_urls', models.JSONField()),
            ],
        ),
    ]