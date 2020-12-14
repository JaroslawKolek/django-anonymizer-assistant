from django.contrib.auth.models import models, AbstractUser

from anonymizer.models import AnonymizerModel


class UserAddress(AnonymizerModel):
    street = models.TextField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)

    class AnonymizerMeta:
        anonymizer_fields = ['street']

    def __str__(self):
        return f'<UserAddress PK:{self.pk} | Street: {self.street} | City: {self.city}>'


class UserSecretData(AnonymizerModel):
    super_secret_data = models.TextField(null=True, blank=True)


class User(AbstractUser, AnonymizerModel):
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, null=True, blank=True)
    secret_data = models.ForeignKey(UserSecretData, on_delete=models.CASCADE, null=True, blank=True)

    class AnonymizerMeta:
        anonymizer_fields = ['address', 'secret_data']
        anonymizer_encode_fields = ['username', 'email']

    def __str__(self):
        return f'<User PK:{self.pk} | Username: {self.username}>'
