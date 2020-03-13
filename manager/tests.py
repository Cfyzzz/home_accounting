from datetime import date, timedelta

from django.test import TestCase

from .models import ManagerCashItems, CashItem


class ManagerCashItemsModelTests(TestCase):
    def test_set_period(self):
        begin_day = date.today()
        end_day = begin_day + timedelta(days=90)
        next_day = begin_day + timedelta(days=30)
        out_day = begin_day + timedelta(days=91)

        cashitem1 = CashItem(name="Тест2", date=begin_day, value=10000)
        cashitem1.save()
        cashitem2 = CashItem(name="Тест3", date=next_day, value=15000)
        cashitem2.save()
        cashitem3 = CashItem(name="Тест4", date=out_day, value=1000)
        cashitem3.save()

        row = ManagerCashItems(date_begin=begin_day, date_end=end_day, cash_item=cashitem1)
        row.save()
        row = ManagerCashItems(date_begin=begin_day, date_end=end_day, cash_item=cashitem2)
        row.save()
        row = ManagerCashItems(date_begin=begin_day, date_end=out_day, cash_item=cashitem3)
        row.save()

        selection = ManagerCashItems.objects.filter(date_begin=begin_day, date_end=end_day)
        summa = sum(item.cash_item.value for item in selection if item.cash_item.name[:4] == 'Тест')
        self.assertEqual(summa, 25000)

    def test_replace(self):
        begin_day = date.today()
        next_day = begin_day + timedelta(days=30)
        end_day = begin_day + timedelta(days=90)

        cashitem1 = CashItem(name="Тест5", date=begin_day, value=10000)
        cashitem1.save()
        cashitem2 = CashItem(name="Тест6", date=next_day, value=15000)
        cashitem2.min_value = 10
        cashitem2.plan_value = 40000
        cashitem2.virtual_value = 3500
        cashitem2.save()

        row = ManagerCashItems(date_begin=begin_day, date_end=end_day, cash_item=cashitem1)
        row.save()

        row.replace(dest_cash_item=cashitem1, source_cash_item=cashitem2)

        cashitem = CashItem.objects.get(name="Тест5")
        self.assertEqual(cashitem.value, 15000)
        self.assertEqual(cashitem.date, next_day)
        self.assertEqual(cashitem.min_value, 10)
        self.assertEqual(cashitem.plan_value, 40000)
        self.assertEqual(cashitem.virtual_value, 3500)

        cashitem = CashItem.objects.get(name="Тест6")
        self.assertEqual(cashitem.value, 15000)
        self.assertEqual(cashitem.date, next_day)
        self.assertEqual(cashitem.min_value, 10)
        self.assertEqual(cashitem.plan_value, 40000)
        self.assertEqual(cashitem.virtual_value, 3500)


    # def test_append(self):
    #     begin_day = date.today()
    #     end_day = begin_day + timedelta(days=90)
    #
    #     cashitem1 = CashItem(name="Тест5", date=begin_day, value=10000)
    #     cashitem1.save()
    #     cashitem2 = CashItem(name="Тест6", date=begin_day, value=15000)
    #     cashitem2.save()
    #
    #     row = ManagerCashItems(date_begin=begin_day, date_end=end_day)
    #     row.append(cashitem1)
    #     row.append(cashitem2)
    #
    #     selection = ManagerCashItems.objects.filter(date_begin=begin_day, date_end=end_day)
    #     val = sum(item.cash_items.value for item in selection if item.cash_items.name[:4] == 'Тест')
    #     self.assertEqual(val, 25000)
