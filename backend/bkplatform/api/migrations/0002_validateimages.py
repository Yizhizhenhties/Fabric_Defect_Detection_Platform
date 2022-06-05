# Generated by Django 3.1.3 on 2022-06-02 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidateImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgurls', models.TextField()),
            ],
            options={
                'verbose_name': '验证图片',
                'verbose_name_plural': '验证图片',
                'db_table': 'validate_imgs',
            },
        ),
    ]