from datetime import date, timedelta

from django.test import TestCase

from .models import ManagerCashItems, CashItem


class ManagerCashItemsModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(ManagerCashItemsModelTests, self).__init__(*args, **kwargs)
        self.begin_day = date.today()
        self.end_day = self.begin_day + timedelta(days=90)
        self.next_day = self.begin_day + timedelta(days=30)
        self.out_day = self.begin_day + timedelta(days=91)

    def test_append(self):
        mgr = ManagerCashItems(date_begin=self.begin_day, date_end=self.end_day)
        mgr.append(name_item="Testing_mci01", date_item=self.begin_day)

        selected = CashItem.objects.filter(date=self.begin_day)
        self.assertTrue(selected.exists())
        self.assertEqual(len(mgr.cash_items), 1)

    def test_set_period(self):
        mgr = ManagerCashItems(date_begin=self.begin_day, date_end=self.end_day)
        mgr.append(name_item="Testing_mcitsp01", date_item=self.begin_day)
        mgr.append(name_item="Testing_mcitsp02", date_item=self.next_day)
        mgr.append(name_item="Testing_mcitsp03", date_item=self.out_day)

        self.assertEqual(len(mgr.cash_items), 2)

    def test_remove(self):
        mgr = ManagerCashItems(date_begin=self.begin_day, date_end=self.end_day)
        mgr.append(name_item="Testing_mcir01", date_item=self.begin_day)
        row = mgr.append(name_item="Testing_mcir02", date_item=self.next_day)
        mgr.append(name_item="Testing_mcir03", date_item=self.out_day)
        mgr.remove(row)

        self.assertEqual(len(mgr.cash_items), 1)

    def test_replace(self):
        mgr = ManagerCashItems(date_begin=self.begin_day, date_end=self.end_day)
        cashitem1 = mgr.append(name_item="Testing_mcir04", date_item=self.begin_day)
        cashitem1.value = 10000
        cashitem1.save()

        cashitem2 = mgr.append(name_item="Testing_mcir05", date_item=self.next_day)
        cashitem2.value = 15000
        cashitem2.min_value = 10
        cashitem2.plan_value = 40000
        cashitem2.virtual_value = 3500
        cashitem2.save()

        mgr.replace(dest_cash_item=cashitem1, source_cash_item=cashitem2)

        self.assertEqual(cashitem1.value, 15000)
        self.assertEqual(cashitem1.date, self.next_day)
        self.assertEqual(cashitem1.min_value, 10)
        self.assertEqual(cashitem1.plan_value, 40000)
        self.assertEqual(cashitem1.virtual_value, 3500)

        self.assertEqual(cashitem2.value, 15000)
        self.assertEqual(cashitem2.date, self.next_day)
        self.assertEqual(cashitem2.min_value, 10)
        self.assertEqual(cashitem2.plan_value, 40000)
        self.assertEqual(cashitem2.virtual_value, 3500)
