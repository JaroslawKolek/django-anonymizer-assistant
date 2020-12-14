from django.test import TestCase

from ..models import UserSecretData


class UserSecretDataBaseSetup(TestCase):
    TEST_SECRET_DATA = 'Gimme a man after midnight!'

    def setUp(self):
        UserSecretData.objects.create(super_secret_data=self.TEST_SECRET_DATA)


class UserAddressBasicTestCase(UserSecretDataBaseSetup):
    def test_user_secret_data_created(self):
        self.assertEqual(UserSecretData.objects.count(), 1)

    def test_user_secret_data_created_with_proper_values(self):
        user_secret_data_obj = UserSecretData.objects.first()

        self.assertEqual(user_secret_data_obj.super_secret_data, self.TEST_SECRET_DATA)


class UserSecretDataAnonymizerTestCase(UserSecretDataBaseSetup):
    def test_anonymize_me(self):
        user_secret_data_obj = UserSecretData.objects.first()

        self.assertEqual(user_secret_data_obj.super_secret_data, self.TEST_SECRET_DATA)
        user_secret_data_obj.anonymize_me()

        # Nothing was specified to anonymized so object was deleted
        self.assertEqual(UserSecretData.objects.count(), 0)
