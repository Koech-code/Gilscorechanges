# Generated by Django 3.2.15 on 2022-11-30 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0020_auto_20221130_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
