# Generated by Django 3.0.4 on 2020-09-30 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('up_app', '0002_order_extradition_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='extradition_date',
            field=models.DateField(blank=True),
        ),
    ]
