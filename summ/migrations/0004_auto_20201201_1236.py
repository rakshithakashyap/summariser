# Generated by Django 3.1.3 on 2020-12-01 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summ', '0003_auto_20201201_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='')),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
