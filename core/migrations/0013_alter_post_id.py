# Generated by Django 4.1.6 on 2023-05-15 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
