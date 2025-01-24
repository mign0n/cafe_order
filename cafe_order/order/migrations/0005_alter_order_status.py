# Generated by Django 5.1.5 on 2025-01-24 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('', '----------'), ('WAITING', 'Waiting'), ('READY', 'Ready'), ('PAID_FOR', 'Paid for')], default='WAITING', max_length=10),
        ),
    ]
