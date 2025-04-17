from django.test import TestCase

from loanmanagement.testing.helpers import create_test_user, create_test_loan
from loans.models import Bank


class GenericTestCase(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(name="Test Bank")

        self.user1 = create_test_user(username="user1")
        self.user2 = create_test_user(username="user2")

        self.loan_for_user1 = create_test_loan(self.user1, self.bank)
        self.loan_for_user2 = create_test_loan(self.user2, self.bank)
