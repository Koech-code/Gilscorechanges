# Generated by Django 3.2.15 on 2022-09-18 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Formula1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='tweet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Formula1_comments', to='Formula1.tweet'),
        ),
    ]