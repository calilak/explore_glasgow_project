# Generated by Django 4.2.11 on 2024-03-22 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_alter_activity_id_alter_category_id_alter_event_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="place",
            name="img_ref",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="place",
            name="slug",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="event",
            name="categories",
            field=models.ManyToManyField(blank=True, to="app.category"),
        ),
        migrations.AlterField(
            model_name="event",
            name="tags",
            field=models.ManyToManyField(blank=True, to="app.tag"),
        ),
        migrations.AlterField(
            model_name="place",
            name="categories",
            field=models.ManyToManyField(blank=True, to="app.category"),
        ),
        migrations.AlterField(
            model_name="place",
            name="tags",
            field=models.ManyToManyField(blank=True, to="app.tag"),
        ),
    ]