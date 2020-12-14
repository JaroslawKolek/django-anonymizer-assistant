from typing import Tuple, List, Optional
from django.db import models

from .anonymizer_crypto import AnonymizerCrypto
from .consts import ANONYMIZER_NONE


class AnonymizerModel(models.Model):
    is_object_anonymized = models.BooleanField(default=False)

    class Meta:
        abstract = True

    class AnonymizerMeta:
        anonymizer_fields = None
        anonymizer_encode_fields = None

    @staticmethod
    def get_instructions(obj) -> Tuple[Optional[List[str]], Optional[List[str]]]:
        fields_to_encode = getattr(obj.AnonymizerMeta, 'anonymizer_encode_fields', None)
        fields_to_anonymize = getattr(obj.AnonymizerMeta, 'anonymizer_fields', None)

        return fields_to_encode, fields_to_anonymize

    def anonymize_me(self):
        anonymizer_crypto: AnonymizerCrypto = AnonymizerCrypto()
        fields_to_encode, fields_to_anonymize = self.get_instructions(self)

        if fields_to_encode is None and fields_to_anonymize is None:
            return self.delete()

        if fields_to_encode:
            for field_name_to_encode in fields_to_encode:
                value_to_encode = getattr(self, field_name_to_encode)
                setattr(self, field_name_to_encode, anonymizer_crypto.encode_value(value_to_encode))

        if fields_to_anonymize:
            for field_name_to_anonymize in fields_to_anonymize:
                field = getattr(self, field_name_to_anonymize)

                if isinstance(field, str):
                    setattr(self, field_name_to_anonymize, ANONYMIZER_NONE)
                else:
                    self.anonymize_related_object(field, field_name_to_anonymize)

        self.is_object_anonymized = True
        return self.save()

    def anonymize_related_object(self, obj, field_name: str):
        if all(v is None for v in self.get_instructions(obj)):
            setattr(self, field_name, ANONYMIZER_NONE)
            return self.delete_object_if_fields_not_specified(obj)
        return obj.anonymize_me()

    @staticmethod
    def delete_object_if_fields_not_specified(obj: models.Model):
        return obj.delete()
