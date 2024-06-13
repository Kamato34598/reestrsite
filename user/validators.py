from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_iin(value):
    if not value.isdigit():
        raise ValidationError(_('ИИН должен состоять только из цифр.'))
    if len(value) != 12:
        raise ValidationError(_('ИИН должен содержать ровно 12 цифр.'))