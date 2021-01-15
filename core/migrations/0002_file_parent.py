# Generated by Django 3.1.5 on 2021-01-15 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='parent',
            field=models.ForeignKey(blank=True, editable=False, help_text='For processed files parent', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.file'),
        ),
    ]
