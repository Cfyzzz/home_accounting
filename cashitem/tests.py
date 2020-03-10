from django.test import TestCase
from django.shortcuts import get_object_or_404

from .models import CashItem


class CashItemModelTests(TestCase):
    def test_set_value(self):
        row = CashItem(name='Тест')
        row.value = 30000
        row.save()

        record = get_object_or_404(CashItem, name='Тест')
        self.assertEqual(record.value, 30000)
