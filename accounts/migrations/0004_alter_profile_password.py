# Generated by Django 4.2.3 on 2023-09-01 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_country_profile_city_profile_gender_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(max_length=1000),
        ),
    ]
