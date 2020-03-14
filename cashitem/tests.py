from django.test import TestCase
from django.shortcuts import get_object_or_404

from .models import CashItem, NamesCashItem


class CashItemModelTests(TestCase):
    def test_set_value(self):
        name_item = NamesCashItem(name=u"Test_aa01")
        name_item.save()
        row = CashItem(name=name_item)
        row.value = 30000
        row.save()

        record = get_object_or_404(CashItem, name=name_item)
        self.assertEqual(record.value, 30000)
