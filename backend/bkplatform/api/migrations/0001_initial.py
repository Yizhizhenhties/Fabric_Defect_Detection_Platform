# Generated by Django 3.1.3 on 2022-05-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': '用户列表',
                'verbose_name_plural': '用户列表',
                'db_table': 'users',
            },
        ),
    ]