# Generated by Django 2.2.4 on 2019-08-30 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0021_auto_20190830_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='image',
            field=models.FileField(default='images/None/no-img.jpg', upload_to='images/'),
        ),
    ]
