from django.test import TestCase

from anonymizer.consts import ANONYMIZER_NULL_EMPTY_VALUES
from ..models import UserAddress


class UserAddressBaseSetup(TestCase):
    TEST_STREET_NAME = 'Abc'
    TEST_CITY_NAME = 'Wro'

    def setUp(self):
        UserAddress.objects.create(
            street=self.TEST_STREET_NAME,
            city=self.TEST_CITY_NAME
        )


class UserAddressBasicTestCase(UserAddressBaseSetup):
    def test_address_created(self):
        self.assertEqual(UserAddress.objects.count(), 1)

    def test_address_created_with_proper_values(self):
        address_obj = UserAddress.objects.first()

        self.assertEqual(address_obj.street, self.TEST_STREET_NAME)
        self.assertEqual(address_obj.city, self.TEST_CITY_NAME)

    def test_address_str_method(self):
        address_obj = UserAddress.objects.first()

        self.assertEqual(
            str(address_obj),
            f'<UserAddress PK:{address_obj.pk} | Street: {self.TEST_STREET_NAME} | City: {self.TEST_CITY_NAME}>'
        )


class UserAddressAnonymizerTestCase(UserAddressBaseSetup):
    def test_anonymize_me(self):
        address_obj = UserAddress.objects.first()

        self.assertEqual(address_obj.street, self.TEST_STREET_NAME)
        self.assertEqual(address_obj.city, self.TEST_CITY_NAME)
        address_obj.anonymize_me()

        address_anonymized_obj = UserAddress.objects.first()
        self.assertIn(address_anonymized_obj.street, ANONYMIZER_NULL_EMPTY_VALUES)
        self.assertEqual(address_anonymized_obj.city, self.TEST_CITY_NAME)
        self.assertTrue(address_anonymized_obj.is_object_anonymized)
