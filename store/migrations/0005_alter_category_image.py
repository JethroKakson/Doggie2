# Generated by Django 5.0.3 on 2024-04-02 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='assets/cover'),
        ),
    ]
