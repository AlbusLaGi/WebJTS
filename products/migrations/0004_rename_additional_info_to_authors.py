# Generated manually to rename additional_info to authors
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_additional_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='additional_info',
            new_name='authors',
        ),
    ]