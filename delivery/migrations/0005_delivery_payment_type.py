# Generated by Django 4.2.3 on 2023-09-12 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_paymentmethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='payment_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pay', to='delivery.paymentmethod'),
        ),
    ]
