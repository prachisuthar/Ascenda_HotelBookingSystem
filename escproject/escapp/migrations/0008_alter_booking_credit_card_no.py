# Generated by Django 3.2.7 on 2022-08-02 07:49

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('escapp', '0007_booking_booking_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='credit_card_no',
            field=django_cryptography.fields.encrypt(models.PositiveIntegerField()),
        ),
    ]
