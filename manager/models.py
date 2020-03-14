from django.db import models

from cashitem.models import CashItem, NamesCashItem


class ManagerCashItems:

    def __init__(self, date_begin, date_end):
        self.date_begin = date_begin
        self.date_end = date_end
        self.cash_items = []
        self.update()

    def __unicode__(self):
        return f"{self.date_begin} - {self.date_end}"

    def set_period_manager(self, begin, end):
        """Установить период текущего менеджера

        :param begin: начало периода
        :param end: конец периода
        """
        self.date_begin = begin
        self.date_end = end
        self.update()

    def append(self, name_item, date_item):
        """Добавить запись в менеджер

        :param date_item: дата записи
        :param name_item: название статьи (строка)
        """
        name_cashitem = NamesCashItem.objects.filter(name=name_item)
        if not name_cashitem.exists():
            name_cashitem = NamesCashItem(name=name_item)
            name_cashitem.save()

        row = CashItem(name=name_cashitem, date=date_item)
        row.save()
        self.update()
        return row

    def remove(self, cash_item):
        """Удалить запись из менеджера

        :param cash_item: удаляемая запись
        """
        cash_item.delete()
        self.update()

    def replace(self, dest_cash_item, source_cash_item):
        """Переписать запись таблицы менеджера

        :param dest_cash_item: запись-приёмник
        :param source_cash_item: запись-источник
        """
        dest_cash_item.min_value = source_cash_item.min_value
        dest_cash_item.value = source_cash_item.value
        dest_cash_item.plan_value = source_cash_item.plan_value
        dest_cash_item.date = source_cash_item.date
        dest_cash_item.virtual_value = source_cash_item.virtual_value
        dest_cash_item.save()

    def copy(self, row):
        """Скопировать запись таблицы менеджера

        :param row: копируемая запись
        :return CashItem: новая запись
        """

    def update(self):
        """Обновить состав статей"""
        self.cash_items = list(CashItem.objects.filter(date__range=(self.date_begin, self.date_end)))

    class Mets:
        verbose_name = u"менеджер планирования"
        verbose_name_plural = u"менеджеры планирования"


class ControlManager(models.Model):
    user = models.CharField(max_length=40)
    manager = models.ForeignKey(CashItem, on_delete=models.CASCADE)

    def create_manager(self):
        """Создать менеджера"""

    def get_managers(self):
        """Получить список менеджеров"""

    def delete_manager(self, manager):
        """Удалить менеджера

        :param manager: удаляемый менеджер
        """

    def copy_manager(self, manager):
        """Копирование менеджера

        :param manager: копируемый менеджер
        :return ManagerCashItems: новый менеджер
        """

    def get_managers_by_date(self, date):
        """Получить всех менеджеров по дате

        :param date: дата, на которую получаем менеджеров
        :return list of ManagerCashItems
        """

    def get_total_manager_by_date(self, date):
        """Получить сводную информацию по всем менеджерам на дату

        :param date: дата, на которую получаем менеджеров
        :return list of CashItem
        """

    def distribute_money(self, rows, money):
        """Разнести приход по статьям

        :param rows: записи, среди которых нужно распределить деньги
        :param money: сумма распределения
        """

    def flow(self, row_source, row_dest):
        """Проводка движения денег между статьями

        :param row_source: запись-источник
        :param row_dest: запись-приёмник
        """
