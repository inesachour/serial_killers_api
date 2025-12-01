# Generated manually to remove duplicate assigned_to columns

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('killers', '0005_modification_assigned_to_serialkiller_assigned_to_and_more'),
    ]

    operations = [
        # Remove duplicate assigned_to column from Suggestions (keep assigned_to_id)
        migrations.RunSQL(
            sql='ALTER TABLE "Suggestions" DROP COLUMN IF EXISTS "assigned_to"',
            reverse_sql='ALTER TABLE "Suggestions" ADD COLUMN "assigned_to" INTEGER',
        ),
        # Remove duplicate assigned_to column from Modifications (keep assigned_to_id)
        migrations.RunSQL(
            sql='ALTER TABLE "Modifications" DROP COLUMN IF EXISTS "assigned_to"',
            reverse_sql='ALTER TABLE "Modifications" ADD COLUMN "assigned_to" INTEGER',
        ),
    ]
