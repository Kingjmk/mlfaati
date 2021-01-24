# Generated by Django 3.1.5 on 2021-01-20 15:50

import common.validators
from django.db import migrations, models
import django.db.models.deletion
import django_lifecycle.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=20, validators=[common.validators.PipelineNameValidator])),
                ('is_enabled', models.BooleanField(db_index=True, default=True)),
                ('target_type', models.CharField(choices=[('ALL', 'All'), ('IMAGE', 'Image'), ('VIDEO', 'Video'), ('AUDIO', 'Audio')], db_index=True, help_text='Select which kind of files to use for this Pipeline', max_length=16)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pipelines', to='core.folder')),
            ],
            options={
                'verbose_name': 'Pipeline',
                'verbose_name_plural': 'Pipelines',
                'ordering': ['-id'],
                'default_permissions': [],
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Transformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('COMPRESS', 'Compress'), ('IMAGE_COMPRESS', 'Compress Image'), ('RESIZE', 'Resize'), ('ADJUST', 'Adjust')], db_index=True, max_length=16)),
                ('extra_data', models.JSONField(blank=True, default=dict, help_text="transformation configuration (Shouldn't) be manually edited)")),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transformations', to='processing.pipeline')),
            ],
            options={
                'verbose_name': 'Transformation',
                'verbose_name_plural': 'Transformations',
                'ordering': ['-id'],
                'default_permissions': [],
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name='pipeline',
            constraint=models.UniqueConstraint(fields=('name', 'folder'), name='processing_pipeline_unique_name_folder'),
        ),
    ]
