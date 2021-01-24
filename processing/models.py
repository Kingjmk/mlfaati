from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_lifecycle import LifecycleModelMixin
import core.models
from common import validators
from . import definitions


class Pipeline(LifecycleModelMixin, models.Model):
    """
    Model to store pipeline for folder,
    purpose of pipeline is to enable running multiple transformations on the same file as a _pipeline_
    and outputting a file as a result
    """

    TYPES = definitions.FileType

    name = models.SlugField(max_length=20, validators=[validators.PipelineNameValidator])
    is_enabled = models.BooleanField(default=True, db_index=True)
    target_type = models.CharField(
        choices=TYPES.choices,
        max_length=16,
        db_index=True,
        help_text=_('Select which kind of files to use for this Pipeline')
    )
    folder: 'core.models.Folder' = models.ForeignKey(
        'core.Folder',
        on_delete=models.CASCADE,
        related_name='pipelines'
    )

    @property
    def _target_type(self) -> definitions.FileType:
        return self.TYPES(self.target_type)

    class Meta:
        constraints = [
            UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_name_folder',
                fields=['name', 'folder'],
            ),
        ]
        ordering = ['-id']
        verbose_name = _('Pipeline')
        verbose_name_plural = _('Pipelines')
        default_permissions = []

    def __str__(self):
        return self.name


class Transformation(LifecycleModelMixin, models.Model):
    """
    Model to store transformation processes for folder
    """
    TYPES = definitions.TransformationType

    pipeline: 'Pipeline' = models.ForeignKey('Pipeline', on_delete=models.CASCADE, related_name='transformations')
    type = models.CharField(choices=TYPES.choices, max_length=16, db_index=True)
    extra_data = models.JSONField(
        default=dict,
        help_text=_("transformation configuration (Shouldn\'t) be manually edited)"),
        blank=True
    )

    @property
    def _type(self) -> definitions.TransformationType:
        return self.TYPES(self.type)

    def process_metadata(self, file):
        return self._type.process_metadata_function(file, **self.extra_data)

    def process_file(self, file):
        return self._type.process_file_function(file, **self.extra_data)

    def clean(self):
        if self.type and self.type not in self.pipeline._target_type.mapping:
            raise ValidationError({'type': _('Type is not supported by selected pipeline.')})

        self.validate_extra_data(self._type.fields, self.extra_data)

    @classmethod
    def validate_extra_data(cls, fields: dict, data: dict):
        # TODO: replace this with serializers or forms
        errors = []
        for field_name, data_types in fields.items():
            if field_name not in data.keys():
                errors += ValidationError(
                    _('Field "%(field_name)s" is required.'), params={'field_name': field_name}, code='required'
                )
                continue

            if not isinstance(data[field_name], data_types):
                errors += ValidationError(
                    _('Field "%(field_name)s "value is not valid, must be of types (%(type)s)'),
                    params={'field_name': field_name, 'type': ', '.join([x.__name__ for x in data_types])}, code='invalid'
                )

        if len(errors) > 0:
            raise ValidationError({'extra_data': errors})

        return data

    class Meta:
        ordering = ['-id']
        verbose_name = _('Transformation')
        verbose_name_plural = _('Transformations')
        default_permissions = []
