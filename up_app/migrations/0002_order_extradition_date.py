# Generated by Django 3.0.4 on 2020-09-30 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('up_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='extradition_date',
            field=models.DateField(default=0),
            preserve_default=False,
        ),
    ]
