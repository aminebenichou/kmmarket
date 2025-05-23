# Generated by Django 5.2 on 2025-04-29 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_order_order_number_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='ORD-2025-d5iscm', editable=False, max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='noimage.jpg', null=True, upload_to='products'),
        ),
    ]
