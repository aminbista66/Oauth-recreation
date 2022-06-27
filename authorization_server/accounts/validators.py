from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone(value):
    if len(value) != 10:
        raise ValidationError(
            _("Given phone number is not valid."),
            params={"value": value})