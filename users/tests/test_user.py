from django.test import TestCase

from anonymizer.consts import ANONYMIZER_NULL_EMPTY_VALUES
from ..models import UserAddress, UserSecretData, User


class UserBaseSetup(TestCase):
    TEST_STREET_NAME = 'Abc'
    TEST_CITY_NAME = 'Wro'

    TEST_SECRET_DATA = 'Gimme a man after midnight!'

    TEST_USERNAME = 'tester'
    TEST_EMAIL = 'email@email.com'

    def setUp(self):
        address = UserAddress.objects.create(
            street=self.TEST_STREET_NAME,
            city=self.TEST_CITY_NAME
        )

        user_secret_data = UserSecretData.objects.create(super_secret_data=self.TEST_SECRET_DATA)

        User.objects.create(
            address=address,
            secret_data=user_secret_data,
            username=self.TEST_USERNAME,
            email=self.TEST_EMAIL,
        )


class UserAddressBasicTestCase(UserBaseSetup):
    def test_user_created(self):
        self.assertEqual(User.objects.count(), 1)

    def test_user_created_with_proper_values(self):
        user_obj = User.objects.first()

        self.assertEqual(user_obj.username, self.TEST_USERNAME)
        self.assertEqual(user_obj.email, self.TEST_EMAIL)

    def test_user_str_method(self):
        user_obj = User.objects.first()

        self.assertEqual(
            str(user_obj),
            f'<User PK:{user_obj.pk} | Username: {self.TEST_USERNAME}>'
        )


class UserAnonymizerTestCase(UserBaseSetup):
    def test_anonymize_me(self):
        user_obj = User.objects.first()

        self.assertEqual(user_obj.username, self.TEST_USERNAME)
        self.assertEqual(user_obj.email, self.TEST_EMAIL)

        user_obj.anonymize_me()

        anonymized_user_obj = User.objects.first()
        self.assertEqual(anonymized_user_obj.username, 'ENCODED: anonymizer pass')
        self.assertEqual(anonymized_user_obj.email, 'ENCODED: anonymizer pass')  # TODO: Fix it when crypto tool will be ready
        self.assertTrue(anonymized_user_obj.is_object_anonymized)


class UserAnonymizerFullFlowTestCase(UserBaseSetup):
    def test_anonymize_full_user_flow(self):
        user_obj = User.objects.first()

        self.assertEqual(user_obj.username, self.TEST_USERNAME)
        self.assertEqual(user_obj.email, self.TEST_EMAIL)

        self.assertEqual(user_obj.address.street, self.TEST_STREET_NAME)
        self.assertEqual(user_obj.address.city, self.TEST_CITY_NAME)

        self.assertEqual(user_obj.secret_data.super_secret_data, self.TEST_SECRET_DATA)

        user_obj.anonymize_me()

        anonymized_user_obj = User.objects.first()
        anonymized_addres_obj = UserAddress.objects.first()

        # UserSecretData should be deleted
        self.assertEqual(UserSecretData.objects.count(), 0)

        self.assertEqual(anonymized_user_obj.username, 'ENCODED: anonymizer pass')
        self.assertEqual(anonymized_user_obj.email, 'ENCODED: anonymizer pass')  # TODO: Fix it when crypto tool will be ready

        self.assertIn(anonymized_addres_obj.street, ANONYMIZER_NULL_EMPTY_VALUES)
        self.assertEqual(anonymized_addres_obj.city, self.TEST_CITY_NAME)

        self.assertTrue(anonymized_user_obj.is_object_anonymized)
