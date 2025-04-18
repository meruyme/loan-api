from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class GreaterThanValueValidator(BaseValidator):
    message = _('Ensure this value is greater than %(limit_value)s.')
    code = 'greater_than_value'

    def compare(self, a, b):
        return a <= b
