# Generated by Django 2.0.7 on 2018-08-25 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_box'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='ownerUserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='boxes', to='api.User'),
        ),
    ]