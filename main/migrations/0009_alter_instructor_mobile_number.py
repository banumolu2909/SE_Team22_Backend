# Generated by Django 4.1.7 on 2023-04-08 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_instructor_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='mobile_number',
            field=models.BigIntegerField(),
        ),
    ]
