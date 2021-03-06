# Generated by Django 3.1.5 on 2021-04-11 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('processing', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='pipeline',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='processing.pipeline'),
        ),
        migrations.AddField(
            model_name='file',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='core.space'),
        ),
        migrations.AlterIndexTogether(
            name='space',
            index_together={('name', 'owner')},
        ),
        migrations.AddConstraint(
            model_name='folder',
            constraint=models.UniqueConstraint(condition=models.Q(parent__isnull=True), fields=('name',), name='core_folder_unique_name_parent_nullable'),
        ),
        migrations.AddConstraint(
            model_name='folder',
            constraint=models.UniqueConstraint(fields=('name', 'parent'), name='core_folder_unique_name_parent'),
        ),
        migrations.AlterIndexTogether(
            name='folder',
            index_together={('path', 'space')},
        ),
        migrations.AddConstraint(
            model_name='file',
            constraint=models.UniqueConstraint(condition=models.Q(folder__isnull=True), fields=('name',), name='core_file_unique_name_folder_nullable'),
        ),
        migrations.AddConstraint(
            model_name='file',
            constraint=models.UniqueConstraint(fields=('name', 'folder'), name='core_file_unique_name_folder'),
        ),
        migrations.AlterIndexTogether(
            name='file',
            index_together={('name', 'folder'), ('name', 'folder', 'space')},
        ),
    ]
