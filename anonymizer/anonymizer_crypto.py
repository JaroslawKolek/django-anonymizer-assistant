from django.conf import settings


class AnonymizerCrypto:
    def encode_value(self, text: str) -> str:
        """ Here should be implemented some cryptography tool to encode/decode stuff """
        password = settings.ANONYMIZER_SECRET_KEY
        return f'ENCODED: {password}'

    def decode_value(self, text: str) -> str:
        raise NotImplementedError
