from datetime import date, timedelta

from django.test import TestCase

from controlmgr.models import ControlManager
from manager.models import ManagerCashItems


class ControlManagerTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(ControlManagerTests, self).__init__(*args, **kwargs)
        self.begin_day = date.today()
        self.end_day = self.begin_day + timedelta(days=90)
        self.next_day = self.begin_day + timedelta(days=30)
        self.out_day = self.begin_day + timedelta(days=91)

    def test_flow(self):
        cmgr = ControlManager()
        mgr = ManagerCashItems(date_begin=self.begin_day, date_end=self.end_day)
        cashitem1 = mgr.append(name_item="Testing_cmttf01", date_item=self.begin_day)
        cashitem1.value = 10000
        cashitem1.save()

        cashitem2 = mgr.append(name_item="Testing_cmttf02", date_item=self.next_day)

        result = cmgr.flow(row_source=cashitem2, row_dest=cashitem1, summa=5000)
        self.assertFalse(result)

        result = cmgr.flow(row_source=cashitem1, row_dest=cashitem2, summa=5000)
        self.assertTrue(result)
